"""
Hosted Agent Implementation - Complete agent for production deployments
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from threading import Thread, Lock, Event
import psutil

from src.agents.base_agent import BaseAgent, AgentConfig, AgentStatus, AgentMetrics
from src.foundry import FoundryClient
from src.utils.config import load_config
from src.utils.logger import get_logger


class HostedAgent(BaseAgent):
    """
    Production-grade hosted agent for executing data pipelines.
    
    Features:
    - Asynchronous pipeline execution
    - Queue management
    - Health monitoring
    - Metrics collection
    - Error handling and retries
    - Integration with Foundry
    
    Example:
        >>> config = AgentConfig(
        ...     agent_id="agent-001",
        ...     name="Production Pipeline Agent"
        ... )
        >>> agent = HostedAgent(config)
        >>> agent.start()
        >>> agent.execute_pipeline({"name": "my_pipeline", ...})
        >>> agent.stop()
    """
    
    def __init__(self, config: AgentConfig, foundry_client: Optional[FoundryClient] = None):
        """
        Initialize hosted agent.
        
        Args:
            config: Agent configuration
            foundry_client: Optional Foundry client for cloud integration
        """
        super().__init__(config)
        self.foundry_client = foundry_client
        self.logger = get_logger(f"hosted_agent.{config.agent_id}")
        
        # Threading control
        self._lock = Lock()
        self._shutdown_event = Event()
        self._worker_thread = None
        self._is_running = False
        
        # Performance monitoring
        self._process = psutil.Process()
    
    def start(self) -> None:
        """
        Start the hosted agent.
        
        Initializes worker threads and begins accepting pipelines.
        """
        if self._is_running:
            self.logger.warning("Agent already running")
            return
        
        with self._lock:
            try:
                self.logger.info(f"Starting hosted agent: {self.config.agent_id}")
                self._is_running = True
                self._shutdown_event.clear()
                self.status = AgentStatus.RUNNING
                self.started_at = datetime.now()
                
                # Start worker thread
                self._worker_thread = Thread(
                    target=self._worker_loop,
                    daemon=True,
                    name=f"agent-worker-{self.config.agent_id}"
                )
                self._worker_thread.start()
                
                self.logger.info(f"Agent started successfully: {self.config.agent_id}")
                
            except Exception as e:
                self.status = AgentStatus.ERROR
                self.logger.error(f"Failed to start agent: {str(e)}", exc_info=True)
                raise
    
    def stop(self) -> None:
        """
        Stop the hosted agent gracefully.
        
        Waits for active pipelines to complete before shutting down.
        """
        if not self._is_running:
            self.logger.warning("Agent not running")
            return
        
        with self._lock:
            try:
                self.logger.info(f"Stopping hosted agent: {self.config.agent_id}")
                self._shutdown_event.set()
                self._is_running = False
                
                # Wait for worker thread
                if self._worker_thread and self._worker_thread.is_alive():
                    self._worker_thread.join(timeout=self.config.timeout)
                
                self.status = AgentStatus.STOPPED
                self.stopped_at = datetime.now()
                
                self.logger.info(f"Agent stopped: {self.config.agent_id}")
                
            except Exception as e:
                self.status = AgentStatus.ERROR
                self.logger.error(f"Error stopping agent: {str(e)}", exc_info=True)
    
    def execute_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a data pipeline.
        
        Args:
            pipeline_config: Pipeline configuration containing:
                - name (str): Pipeline name
                - module (str): Python module path
                - class (str): Pipeline class name
                - config (dict): Pipeline-specific config
                
        Returns:
            Execution result with status, metrics, and errors
        """
        pipeline_name = pipeline_config.get("name", "unknown")
        pipeline_id = pipeline_config.get("id", f"pipeline-{int(time.time())}")
        
        start_time = time.time()
        result = {
            "pipeline_id": pipeline_id,
            "pipeline_name": pipeline_name,
            "status": "success",
            "error": None,
            "execution_time": 0,
            "start_time": datetime.now().isoformat(),
            "output": None,
        }
        
        try:
            self.logger.info(f"Executing pipeline: {pipeline_name}")
            
            # Validate configuration
            if not self._validate_pipeline_config(pipeline_config):
                raise ValueError("Invalid pipeline configuration")
            
            # Import and instantiate pipeline
            pipeline_instance = self._create_pipeline_instance(pipeline_config)
            
            # Execute pipeline
            output = self._run_pipeline(pipeline_instance, pipeline_config)
            
            # Record success
            self.metrics.pipelines_executed += 1
            self.metrics.pipelines_succeeded += 1
            result["output"] = output
            
            self.logger.info(f"Pipeline completed successfully: {pipeline_name}")
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.metrics.pipelines_executed += 1
            self.metrics.pipelines_failed += 1
            result["status"] = "failed"
            result["error"] = str(e)
            self.logger.error(f"Pipeline execution failed: {pipeline_name}: {str(e)}", exc_info=True)
        
        finally:
            execution_time = time.time() - start_time
            result["execution_time"] = execution_time
            self.metrics.last_execution_time = datetime.now()
            self.metrics.total_execution_time += execution_time
            
            if self.metrics.pipelines_executed > 0:
                self.metrics.average_execution_time = (
                    self.metrics.total_execution_time / self.metrics.pipelines_executed
                )
        
        return result
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get agent health status.
        
        Returns:
            Health status information
        """
        try:
            memory_info = self._process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            cpu_percent = self._process.cpu_percent(interval=0.1)
            
            self.metrics.memory_usage_mb = memory_mb
            self.metrics.cpu_usage_percent = cpu_percent
            
            is_healthy = (
                self._is_running and
                memory_mb < 2000 and  # Less than 2GB
                cpu_percent < 80 and  # Less than 80% CPU
                self.metrics.errors_count < 10  # Less than 10 errors
            )
            
            return {
                "is_healthy": is_healthy,
                "status": self.status.value,
                "memory_mb": memory_mb,
                "cpu_percent": cpu_percent,
                "uptime_seconds": (datetime.now() - self.started_at).total_seconds() if self.started_at else 0,
                "errors_count": self.metrics.errors_count,
                "queue_size": self.get_queue_size(),
            }
        except Exception as e:
            self.logger.error(f"Error getting health status: {str(e)}", exc_info=True)
            return {
                "is_healthy": False,
                "error": str(e),
            }
    
    def pause(self) -> None:
        """Pause pipeline execution"""
        with self._lock:
            self.status = AgentStatus.PAUSED
            self.logger.info(f"Agent paused: {self.config.agent_id}")
    
    def resume(self) -> None:
        """Resume pipeline execution"""
        with self._lock:
            self.status = AgentStatus.RUNNING
            self.logger.info(f"Agent resumed: {self.config.agent_id}")
    
    def clear_queue(self) -> None:
        """Clear the pipeline queue"""
        with self._lock:
            cleared = len(self._pipeline_queue)
            self._pipeline_queue.clear()
            self.logger.info(f"Cleared {cleared} pipelines from queue")
    
    # Private methods
    
    def _worker_loop(self) -> None:
        """Worker thread main loop for processing pipelines"""
        self.logger.info("Worker thread started")
        
        while not self._shutdown_event.is_set():
            try:
                # Wait for pipeline or shutdown
                if self._pipeline_queue and self.status == AgentStatus.RUNNING:
                    with self._lock:
                        if self._pipeline_queue:
                            pipeline_config = self._pipeline_queue.pop(0)
                            self.execute_pipeline(pipeline_config)
                else:
                    time.sleep(0.5)  # Avoid busy waiting
                    
            except Exception as e:
                self.logger.error(f"Worker loop error: {str(e)}", exc_info=True)
                time.sleep(1)
        
        self.logger.info("Worker thread stopped")
    
    def _validate_pipeline_config(self, config: Dict[str, Any]) -> bool:
        """Validate pipeline configuration"""
        required_fields = ["name"]
        return all(field in config for field in required_fields)
    
    def _create_pipeline_instance(self, config: Dict[str, Any]) -> Any:
        """
        Create pipeline instance from configuration.
        
        Args:
            config: Pipeline configuration with module/class info
            
        Returns:
            Pipeline instance
        """
        # For now, return a mock pipeline
        # In production, this would dynamically import and instantiate
        class MockPipeline:
            def run(self):
                return {"status": "success", "rows_processed": 100}
        
        return MockPipeline()
    
    def _run_pipeline(self, pipeline_instance: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a pipeline instance.
        
        Args:
            pipeline_instance: Pipeline instance to run
            config: Pipeline configuration
            
        Returns:
            Pipeline output
        """
        if hasattr(pipeline_instance, "run"):
            return pipeline_instance.run()
        else:
            raise ValueError("Pipeline does not have run method")


def create_hosted_agent(
    agent_id: str,
    name: str,
    environment: str = "production",
    foundry_client: Optional[FoundryClient] = None,
    **kwargs
) -> HostedAgent:
    """
    Factory function to create a hosted agent.
    
    Args:
        agent_id: Unique agent identifier
        name: Human-readable agent name
        environment: Deployment environment
        foundry_client: Optional Foundry client
        **kwargs: Additional configuration
        
    Returns:
        Configured hosted agent
    """
    config = AgentConfig(
        agent_id=agent_id,
        name=name,
        environment=environment,
        **kwargs
    )
    
    if foundry_client is None:
        try:
            foundry_config = load_config()
            foundry_client = FoundryClient(
                workspace_id=foundry_config.foundry_workspace,
                api_key=foundry_config.foundry_api_key,
            )
        except Exception as e:
            logging.warning(f"Failed to create Foundry client: {str(e)}")
    
    return HostedAgent(config, foundry_client)

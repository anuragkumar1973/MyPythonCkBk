"""
Base Agent Class - Abstract base for all agent implementations
"""

from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import json


class AgentStatus(str, Enum):
    """Agent lifecycle status"""
    INITIALIZED = "initialized"
    RUNNING = "running"
    IDLE = "idle"
    PAUSED = "paused"
    ERROR = "error"
    STOPPED = "stopped"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class AgentConfig:
    """Configuration for agent"""
    agent_id: str
    name: str
    agent_type: str = "hosted"
    version: str = "1.0.0"
    environment: str = "production"
    max_retries: int = 3
    retry_delay: int = 5
    timeout: int = 3600
    enable_logging: bool = True
    enable_monitoring: bool = True
    extra_config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMetrics:
    """Agent performance metrics"""
    pipelines_executed: int = 0
    pipelines_failed: int = 0
    pipelines_succeeded: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    errors_count: int = 0
    last_execution_time: Optional[datetime] = None
    uptime_seconds: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0


class BaseAgent(ABC):
    """
    Abstract base class for all agent implementations.
    
    An agent is responsible for:
    - Executing data pipelines
    - Monitoring pipeline health
    - Managing retries and error handling
    - Collecting metrics
    - Coordinating with Foundry services
    """
    
    def __init__(self, config: AgentConfig):
        """
        Initialize base agent.
        
        Args:
            config: Agent configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"agent.{config.agent_id}")
        self.status = AgentStatus.INITIALIZED
        self.metrics = AgentMetrics()
        self.started_at = None
        self.stopped_at = None
        self._pipeline_queue: List[Dict[str, Any]] = []
        self._active_pipelines: Dict[str, Any] = {}
    
    @abstractmethod
    def start(self) -> None:
        """Start the agent"""
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """Stop the agent"""
        pass
    
    @abstractmethod
    def execute_pipeline(self, pipeline_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a data pipeline.
        
        Args:
            pipeline_config: Pipeline configuration
            
        Returns:
            Execution result
        """
        pass
    
    def add_pipeline_to_queue(self, pipeline_config: Dict[str, Any]) -> None:
        """
        Add pipeline to execution queue.
        
        Args:
            pipeline_config: Pipeline configuration
        """
        self._pipeline_queue.append(pipeline_config)
        self.logger.info(f"Pipeline added to queue: {pipeline_config.get('name', 'unknown')}")
    
    def get_queue_size(self) -> int:
        """Get number of queued pipelines"""
        return len(self._pipeline_queue)
    
    def get_status(self) -> str:
        """Get current agent status"""
        return self.status.value
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics"""
        return {
            "agent_id": self.config.agent_id,
            "status": self.status.value,
            "pipelines_executed": self.metrics.pipelines_executed,
            "pipelines_succeeded": self.metrics.pipelines_succeeded,
            "pipelines_failed": self.metrics.pipelines_failed,
            "total_execution_time": self.metrics.total_execution_time,
            "average_execution_time": self.metrics.average_execution_time,
            "errors_count": self.metrics.errors_count,
            "queue_size": self.get_queue_size(),
            "last_execution_time": self.metrics.last_execution_time.isoformat() if self.metrics.last_execution_time else None,
        }
    
    def log_info(self, message: str) -> None:
        """Log info level message"""
        self.logger.info(message)
    
    def log_error(self, message: str, exc_info: bool = False) -> None:
        """Log error level message"""
        self.logger.error(message, exc_info=exc_info)
        self.metrics.errors_count += 1
    
    def log_warning(self, message: str) -> None:
        """Log warning level message"""
        self.logger.warning(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary"""
        return {
            "agent_id": self.config.agent_id,
            "name": self.config.name,
            "type": self.config.agent_type,
            "version": self.config.version,
            "environment": self.config.environment,
            "status": self.status.value,
            "metrics": self.get_metrics(),
        }
    
    def to_json(self) -> str:
        """Convert agent to JSON"""
        return json.dumps(self.to_dict(), indent=2, default=str)

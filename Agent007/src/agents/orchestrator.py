"""
Agent Orchestrator - Manage multiple agents and coordinate execution
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json

from src.agents.base_agent import BaseAgent, AgentStatus
from src.agents.hosted_agent import HostedAgent, create_hosted_agent
from src.utils.logger import get_logger


@dataclass
class OrchestrationConfig:
    """Configuration for agent orchestrator"""
    max_concurrent_agents: int = 10
    agent_timeout: int = 3600
    enable_autoscaling: bool = False
    enable_load_balancing: bool = True
    health_check_interval: int = 60


class AgentOrchestrator:
    """
    Manages multiple hosted agents and coordinates pipeline execution.
    
    Features:
    - Multi-agent management
    - Load balancing
    - Health monitoring
    - Automatic scaling
    - Centralized logging
    
    Example:
        >>> orchestrator = AgentOrchestrator()
        >>> agent = orchestrator.create_agent("agent-001", "Primary Agent")
        >>> agent.start()
        >>> orchestrator.submit_pipeline({"name": "pipeline-1"}, "agent-001")
        >>> orchestrator.get_status()
    """
    
    def __init__(self, config: Optional[OrchestrationConfig] = None):
        """
        Initialize agent orchestrator.
        
        Args:
            config: Orchestration configuration
        """
        self.config = config or OrchestrationConfig()
        self.logger = get_logger("agent_orchestrator")
        self._agents: Dict[str, BaseAgent] = {}
        self._execution_history: List[Dict[str, Any]] = []
    
    def create_agent(
        self,
        agent_id: str,
        name: str,
        agent_type: str = "hosted",
        environment: str = "production",
        **kwargs
    ) -> BaseAgent:
        """
        Create and register a new agent.
        
        Args:
            agent_id: Unique agent identifier
            name: Human-readable agent name
            agent_type: Type of agent (hosted, distributed, etc.)
            environment: Deployment environment
            **kwargs: Additional configuration
            
        Returns:
            Created agent instance
        """
        if agent_id in self._agents:
            raise ValueError(f"Agent {agent_id} already exists")
        
        if agent_type != "hosted":
            raise NotImplementedError(f"Agent type {agent_type} not implemented")
        
        agent = create_hosted_agent(
            agent_id=agent_id,
            name=name,
            environment=environment,
            **kwargs
        )
        
        self._agents[agent_id] = agent
        self.logger.info(f"Agent created: {agent_id} - {name}")
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self._agents.get(agent_id)
    
    def list_agents(self) -> List[BaseAgent]:
        """List all agents"""
        return list(self._agents.values())
    
    def submit_pipeline(
        self,
        pipeline_config: Dict[str, Any],
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit pipeline to an agent for execution.
        
        Args:
            pipeline_config: Pipeline configuration
            agent_id: Specific agent ID (optional, uses load balancing)
            
        Returns:
            Submission result with assignment info
        """
        if not self._agents:
            raise ValueError("No agents available")
        
        # Select agent
        if agent_id:
            agent = self.get_agent(agent_id)
            if not agent:
                raise ValueError(f"Agent {agent_id} not found")
        else:
            agent = self._select_agent_for_load_balancing()
        
        if agent.status != AgentStatus.RUNNING:
            raise ValueError(f"Agent {agent.config.agent_id} is not running")
        
        # Submit pipeline
        agent.add_pipeline_to_queue(pipeline_config)
        
        result = {
            "status": "submitted",
            "pipeline_name": pipeline_config.get("name"),
            "agent_id": agent.config.agent_id,
            "queue_position": agent.get_queue_size(),
            "timestamp": datetime.now().isoformat(),
        }
        
        self.logger.info(f"Pipeline submitted: {pipeline_config.get('name')} to {agent.config.agent_id}")
        self._execution_history.append(result)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                agent_id: agent.get_status()
                for agent_id, agent in self._agents.items()
            },
            "agents_count": len(self._agents),
            "running_agents": sum(
                1 for agent in self._agents.values()
                if agent.status == AgentStatus.RUNNING
            ),
            "total_pipelines_executed": sum(
                agent.metrics.pipelines_executed
                for agent in self._agents.values()
            ),
        }
    
    def get_health(self) -> Dict[str, Any]:
        """Get orchestrator health"""
        health_status = {}
        for agent_id, agent in self._agents.items():
            if hasattr(agent, "get_health_status"):
                health_status[agent_id] = agent.get_health_status()
        
        is_healthy = all(
            status.get("is_healthy", False)
            for status in health_status.values()
        )
        
        return {
            "is_healthy": is_healthy,
            "agents_health": health_status,
            "timestamp": datetime.now().isoformat(),
        }
    
    def start_all(self) -> None:
        """Start all agents"""
        self.logger.info("Starting all agents")
        for agent in self._agents.values():
            try:
                agent.start()
                self.logger.info(f"Agent started: {agent.config.agent_id}")
            except Exception as e:
                self.logger.error(f"Failed to start agent {agent.config.agent_id}: {str(e)}")
    
    def stop_all(self) -> None:
        """Stop all agents"""
        self.logger.info("Stopping all agents")
        for agent in self._agents.values():
            try:
                agent.stop()
                self.logger.info(f"Agent stopped: {agent.config.agent_id}")
            except Exception as e:
                self.logger.error(f"Error stopping agent {agent.config.agent_id}: {str(e)}")
    
    def get_execution_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self._execution_history[-limit:]
    
    # Private methods
    
    def _select_agent_for_load_balancing(self) -> BaseAgent:
        """Select agent with least load for load balancing"""
        running_agents = [
            agent for agent in self._agents.values()
            if agent.status == AgentStatus.RUNNING
        ]
        
        if not running_agents:
            raise ValueError("No running agents available")
        
        # Select agent with smallest queue
        return min(running_agents, key=lambda a: a.get_queue_size())


def create_orchestrator(
    num_agents: int = 3,
    agent_name_prefix: str = "agent",
    config: Optional[OrchestrationConfig] = None
) -> AgentOrchestrator:
    """
    Factory function to create orchestrator with agents.
    
    Args:
        num_agents: Number of agents to create
        agent_name_prefix: Prefix for agent names
        config: Orchestration configuration
        
    Returns:
        Configured orchestrator with agents
    """
    orchestrator = AgentOrchestrator(config)
    
    for i in range(num_agents):
        agent_id = f"{agent_name_prefix}-{i:03d}"
        agent_name = f"{agent_name_prefix.title()} {i}"
        orchestrator.create_agent(agent_id, agent_name)
    
    return orchestrator

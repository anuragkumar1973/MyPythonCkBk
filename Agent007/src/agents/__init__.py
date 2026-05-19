"""
Agents Module - Hosted agents for pipeline orchestration and monitoring

This module provides hosted agent implementations for managing and executing
data pipelines in distributed environments (Azure, Kubernetes, etc.).
"""

from .base_agent import BaseAgent, AgentStatus
from .hosted_agent import HostedAgent

__all__ = ["BaseAgent", "AgentStatus", "HostedAgent"]

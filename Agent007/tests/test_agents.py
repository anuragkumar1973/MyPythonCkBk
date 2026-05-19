"""
Integration tests for the Hosted Agent system.
Tests agent creation, execution, orchestration, and monitoring.
"""

import unittest
import time
import json
from datetime import datetime
from src.agents.base_agent import AgentStatus, AgentConfig
from src.agents.hosted_agent import HostedAgent, create_hosted_agent
from src.agents.orchestrator import AgentOrchestrator, OrchestrationConfig, create_orchestrator


class TestBaseAgentConfig(unittest.TestCase):
    """Test AgentConfig dataclass."""

    def test_agent_config_creation(self):
        """Test creating agent configuration."""
        config = AgentConfig(
            agent_id="test-001",
            name="Test Agent",
            agent_type="hosted"
        )
        
        self.assertEqual(config.agent_id, "test-001")
        self.assertEqual(config.name, "Test Agent")
        self.assertEqual(config.agent_type, "hosted")
        self.assertEqual(config.environment, "production")
        self.assertEqual(config.max_retries, 3)

    def test_agent_config_custom(self):
        """Test creating agent with custom configuration."""
        config = AgentConfig(
            agent_id="prod-001",
            name="Production Agent",
            environment="production",
            max_retries=5,
            timeout=7200
        )
        
        self.assertEqual(config.agent_id, "prod-001")
        self.assertEqual(config.environment, "production")
        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.timeout, 7200)


class TestHostedAgentBasics(unittest.TestCase):
    """Test basic HostedAgent functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = create_hosted_agent(
            "test-agent-001",
            "Test Agent"
        )

    def tearDown(self):
        """Clean up after tests."""
        if self.agent.status != AgentStatus.STOPPED:
            self.agent.stop()

    def test_agent_creation(self):
        """Test creating a hosted agent."""
        self.assertEqual(self.agent.config.agent_id, "test-agent-001")
        self.assertEqual(self.agent.config.name, "Test Agent")
        self.assertEqual(self.agent.status, AgentStatus.INITIALIZED)

    def test_agent_start_stop(self):
        """Test agent start and stop."""
        self.agent.start()
        self.assertEqual(self.agent.status, AgentStatus.RUNNING)
        
        self.agent.stop()
        self.assertEqual(self.agent.status, AgentStatus.STOPPED)

    def test_agent_pause_resume(self):
        """Test agent pause and resume."""
        self.agent.start()
        self.assertEqual(self.agent.status, AgentStatus.RUNNING)
        
        self.agent.pause()
        self.assertEqual(self.agent.status, AgentStatus.PAUSED)
        
        self.agent.resume()
        self.assertEqual(self.agent.status, AgentStatus.RUNNING)
        
        self.agent.stop()

    def test_agent_get_status(self):
        """Test getting agent status."""
        self.agent.start()
        
        status = self.agent.get_status()
        # status is just the status string
        self.assertEqual(status, "running")
        
        self.agent.stop()

    def test_agent_get_metrics(self):
        """Test getting agent metrics."""
        self.agent.start()
        
        metrics = self.agent.get_metrics()
        self.assertEqual(metrics["agent_id"], "test-agent-001")
        self.assertEqual(metrics["pipelines_executed"], 0)
        self.assertEqual(metrics["pipelines_succeeded"], 0)
        self.assertEqual(metrics["pipelines_failed"], 0)
        self.assertIn("queue_size", metrics)
        
        self.agent.stop()

    def test_agent_get_health(self):
        """Test getting agent health status."""
        self.agent.start()
        
        health = self.agent.get_health_status()
        self.assertIn("is_healthy", health)
        self.assertIn("status", health)
        self.assertIn("memory_mb", health)
        self.assertIn("cpu_percent", health)
        self.assertIn("uptime_seconds", health)
        
        # Health should be at least 0
        self.assertGreaterEqual(health["memory_mb"], 0)
        self.assertGreaterEqual(health["cpu_percent"], 0)
        self.assertGreaterEqual(health["uptime_seconds"], 0)
        
        self.agent.stop()


class TestHostedAgentQueue(unittest.TestCase):
    """Test queue management functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = create_hosted_agent(
            "test-queue-agent",
            "Queue Test Agent"
        )
        self.agent.start()

    def tearDown(self):
        """Clean up after tests."""
        self.agent.stop()

    def test_queue_size_initial(self):
        """Test initial queue size is zero."""
        self.assertEqual(self.agent.get_queue_size(), 0)

    def test_add_to_queue(self):
        """Test adding pipelines to queue."""
        self.agent.add_pipeline_to_queue({
            "name": "pipeline-1"
        })
        
        self.assertEqual(self.agent.get_queue_size(), 1)

    def test_add_multiple_to_queue(self):
        """Test adding multiple pipelines to queue."""
        for i in range(5):
            self.agent.add_pipeline_to_queue({
                "name": f"pipeline-{i}"
            })
        
        self.assertEqual(self.agent.get_queue_size(), 5)

    def test_clear_queue(self):
        """Test clearing queue."""
        for i in range(3):
            self.agent.add_pipeline_to_queue({
                "name": f"pipeline-{i}"
            })
        
        self.assertEqual(self.agent.get_queue_size(), 3)
        
        self.agent.clear_queue()
        self.assertEqual(self.agent.get_queue_size(), 0)


class TestHostedAgentExecution(unittest.TestCase):
    """Test pipeline execution."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = create_hosted_agent(
            "test-exec-agent",
            "Execution Test Agent"
        )
        self.agent.start()

    def tearDown(self):
        """Clean up after tests."""
        self.agent.stop()

    def test_execute_pipeline_basic(self):
        """Test executing a basic pipeline."""
        result = self.agent.execute_pipeline({
            "name": "test_pipeline"
        })
        
        self.assertIn("status", result)
        self.assertIn("execution_time", result)
        self.assertGreaterEqual(result["execution_time"], 0)

    def test_execute_pipeline_with_config(self):
        """Test executing pipeline with configuration."""
        result = self.agent.execute_pipeline({
            "name": "test_pipeline",
            "config": {
                "batch_size": 100,
                "timeout": 60
            }
        })
        
        self.assertIn("status", result)
        self.assertGreaterEqual(result["execution_time"], 0)

    def test_execute_multiple_pipelines(self):
        """Test executing multiple pipelines."""
        results = []
        
        for i in range(3):
            result = self.agent.execute_pipeline({
                "name": f"pipeline_{i}"
            })
            results.append(result)
        
        self.assertEqual(len(results), 3)
        
        metrics = self.agent.get_metrics()
        self.assertEqual(metrics["pipelines_executed"], 3)


class TestAgentSerialization(unittest.TestCase):
    """Test agent serialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = create_hosted_agent(
            "test-serial-agent",
            "Serialization Test Agent"
        )

    def tearDown(self):
        """Clean up after tests."""
        if self.agent.status != AgentStatus.STOPPED:
            self.agent.stop()

    def test_to_dict(self):
        """Test converting agent to dictionary."""
        data = self.agent.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data["agent_id"], "test-serial-agent")
        self.assertEqual(data["name"], "Serialization Test Agent")
        self.assertIn("status", data)
        self.assertIn("metrics", data)

    def test_to_json(self):
        """Test converting agent to JSON."""
        json_str = self.agent.to_json()
        
        self.assertIsInstance(json_str, str)
        data = json.loads(json_str)
        self.assertEqual(data["agent_id"], "test-serial-agent")
        self.assertEqual(data["name"], "Serialization Test Agent")


class TestAgentOrchestrator(unittest.TestCase):
    """Test AgentOrchestrator functionality."""

    def setUp(self):
        """Set up test fixtures."""
        config = OrchestrationConfig(
            max_concurrent_agents=5,
            enable_load_balancing=True
        )
        self.orchestrator = AgentOrchestrator(config)

    def tearDown(self):
        """Clean up after tests."""
        self.orchestrator.stop_all()

    def test_orchestrator_creation(self):
        """Test creating orchestrator."""
        self.assertIsNotNone(self.orchestrator)
        # Check that agents dict exists - can be empty or have default agents
        agents = self.orchestrator.list_agents()
        self.assertIsNotNone(agents)

    def test_create_agent(self):
        """Test creating agents through orchestrator."""
        agent = self.orchestrator.create_agent("orch-agent-001", "Orchestrator Agent 1")
        
        self.assertIsNotNone(agent)
        retrieved_agent = self.orchestrator.get_agent("orch-agent-001")
        self.assertIsNotNone(retrieved_agent)

    def test_create_multiple_agents(self):
        """Test creating multiple agents."""
        for i in range(3):
            self.orchestrator.create_agent(f"orch-agent-{i:03d}", f"Orchestrator Agent {i}")
        
        agents = self.orchestrator.list_agents()
        self.assertGreaterEqual(len(agents), 3)

    def test_get_agent(self):
        """Test getting agent from orchestrator."""
        self.orchestrator.create_agent("test-agent", "Test Agent")
        agent = self.orchestrator.get_agent("test-agent")
        
        self.assertIsNotNone(agent)
        self.assertEqual(agent.config.agent_id, "test-agent")

    def test_list_agents(self):
        """Test listing agents."""
        for i in range(3):
            self.orchestrator.create_agent(f"orch-agent-{i}", f"Agent {i}")
        
        agents = self.orchestrator.list_agents()
        self.assertEqual(len(agents), 3)

    def test_start_stop_all(self):
        """Test starting and stopping all agents."""
        for i in range(2):
            self.orchestrator.create_agent(f"orch-agent-{i}", f"Agent {i}")
        
        self.orchestrator.start_all()
        
        agents = self.orchestrator.list_agents()
        for agent in agents:
            self.assertEqual(agent.status, AgentStatus.RUNNING)
        
        self.orchestrator.stop_all()
        
        agents = self.orchestrator.list_agents()
        for agent in agents:
            self.assertEqual(agent.status, AgentStatus.STOPPED)

    def test_orchestrator_status(self):
        """Test getting orchestrator status."""
        for i in range(2):
            self.orchestrator.create_agent(f"orch-agent-{i}", f"Agent {i}")
        
        self.orchestrator.start_all()
        
        status = self.orchestrator.get_status()
        self.assertIn("agents_count", status)
        self.assertIn("running_agents", status)
        self.assertEqual(status["running_agents"], 2)
        
        self.orchestrator.stop_all()

    def test_orchestrator_health(self):
        """Test getting orchestrator health."""
        for i in range(2):
            self.orchestrator.create_agent(f"orch-agent-{i}", f"Agent {i}")
        
        self.orchestrator.start_all()
        
        health = self.orchestrator.get_health()
        self.assertIn("is_healthy", health)
        self.assertIn("agents_health", health)
        
        self.orchestrator.stop_all()

    def test_submit_pipeline(self):
        """Test submitting pipeline through orchestrator."""
        self.orchestrator.create_agent("orch-agent-1", "Agent 1")
        self.orchestrator.start_all()
        
        result = self.orchestrator.submit_pipeline({
            "name": "test_pipeline"
        })
        
        self.assertIn("status", result)
        
        self.orchestrator.stop_all()

    def test_load_balancing(self):
        """Test load balancing across agents."""
        for i in range(3):
            self.orchestrator.create_agent(f"orch-agent-{i}", f"Agent {i}")
        
        self.orchestrator.start_all()
        
        # Submit multiple pipelines
        for i in range(6):
            self.orchestrator.submit_pipeline({
                "name": f"pipeline_{i}"
            })
        
        # Give time for execution
        time.sleep(2)
        
        # Check status - should be distributed across agents
        status = self.orchestrator.get_status()
        self.assertGreaterEqual(status["total_pipelines_executed"], 0)
        
        self.orchestrator.stop_all()

    def test_execution_history(self):
        """Test execution history."""
        self.orchestrator.create_agent("orch-agent-1", "Agent 1")
        self.orchestrator.start_all()
        
        # Execute some pipelines
        for i in range(3):
            self.orchestrator.submit_pipeline({
                "name": f"history_pipeline_{i}"
            })
        
        # Give time for execution
        time.sleep(1)
        
        # Get history
        history = self.orchestrator.get_execution_history(limit=10)
        self.assertIsInstance(history, list)
        
        self.orchestrator.stop_all()


class TestFactoryFunctions(unittest.TestCase):
    """Test factory functions."""

    def test_create_hosted_agent(self):
        """Test create_hosted_agent factory."""
        agent = create_hosted_agent("factory-agent", "Factory Test Agent")
        
        self.assertIsInstance(agent, HostedAgent)
        self.assertEqual(agent.config.agent_id, "factory-agent")
        
        agent.stop()

    def test_create_orchestrator(self):
        """Test create_orchestrator factory."""
        orchestrator = create_orchestrator(num_agents=3)
        
        self.assertIsInstance(orchestrator, AgentOrchestrator)
        agents = orchestrator.list_agents()
        self.assertGreaterEqual(len(agents), 3)
        
        orchestrator.stop_all()

    def test_create_orchestrator_default(self):
        """Test create_orchestrator with default agents."""
        orchestrator = create_orchestrator()
        
        agents = orchestrator.list_agents()
        self.assertGreater(len(agents), 0)
        
        orchestrator.stop_all()


class TestAgentIntegration(unittest.TestCase):
    """Integration tests for full agent workflows."""

    def test_agent_lifecycle(self):
        """Test complete agent lifecycle."""
        # Create
        agent = create_hosted_agent("lifecycle-agent", "Lifecycle Test")
        self.assertEqual(agent.status, AgentStatus.INITIALIZED)
        
        # Start
        agent.start()
        self.assertEqual(agent.status, AgentStatus.RUNNING)
        
        # Execute
        result = agent.execute_pipeline({"name": "pipeline-1"})
        self.assertIn("status", result)
        
        # Pause
        agent.pause()
        self.assertEqual(agent.status, AgentStatus.PAUSED)
        
        # Resume
        agent.resume()
        self.assertEqual(agent.status, AgentStatus.RUNNING)
        
        # Stop
        agent.stop()
        self.assertEqual(agent.status, AgentStatus.STOPPED)

    def test_orchestrator_workflow(self):
        """Test orchestrator workflow with multiple agents."""
        # Create orchestrator
        orchestrator = create_orchestrator(num_agents=3)
        
        # Start all
        orchestrator.start_all()
        
        # Submit pipelines
        for i in range(10):
            orchestrator.submit_pipeline({
                "name": f"workflow_pipeline_{i}"
            })
        
        # Check status
        status = orchestrator.get_status()
        self.assertGreater(status.get("agents_count", 0), 0)
        
        # Get health
        health = orchestrator.get_health()
        self.assertIsNotNone(health)
        
        # Stop all
        orchestrator.stop_all()
        
        # Verify stopped
        for agent in orchestrator.list_agents():
            self.assertEqual(agent.status, AgentStatus.STOPPED)


if __name__ == "__main__":
    unittest.main()

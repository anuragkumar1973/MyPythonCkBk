"""
Agent Documentation and Examples
"""

# ==============================================================================
# BASIC USAGE
# ==============================================================================

"""
Create and use a hosted agent:
"""

from src.agents.hosted_agent import HostedAgent, create_hosted_agent
from src.agents.base_agent import AgentConfig, AgentStatus

# Create agent configuration
config = AgentConfig(
    agent_id="agent-001",
    name="Production Pipeline Agent",
    version="1.0.0",
    environment="production",
    max_retries=3,
    timeout=3600
)

# Create agent
agent = HostedAgent(config)

# Start agent
agent.start()

# Submit pipeline
pipeline_config = {
    "name": "data_pipeline",
    "module": "src.pipelines.sample_pipeline",
    "class": "SamplePipeline",
    "config": {"batch_size": 1000}
}

result = agent.execute_pipeline(pipeline_config)
print(f"Pipeline result: {result}")

# Get status
status = agent.get_status()
print(f"Agent status: {status}")

# Get metrics
metrics = agent.get_metrics()
print(f"Agent metrics: {metrics}")

# Stop agent
agent.stop()

# ==============================================================================
# USING FACTORY FUNCTION
# ==============================================================================

"""
Create agent using factory function:
"""

agent = create_hosted_agent(
    agent_id="agent-002",
    name="Secondary Agent",
    environment="staging"
)

agent.start()
agent.stop()

# ==============================================================================
# USING ORCHESTRATOR
# ==============================================================================

"""
Manage multiple agents with orchestrator:
"""

from src.agents.orchestrator import AgentOrchestrator, OrchestrationConfig, create_orchestrator

# Create orchestrator with configuration
orch_config = OrchestrationConfig(
    max_concurrent_agents=10,
    enable_load_balancing=True,
    enable_autoscaling=False
)

orchestrator = AgentOrchestrator(orch_config)

# Create agents
agent1 = orchestrator.create_agent("agent-001", "Primary Agent")
agent2 = orchestrator.create_agent("agent-002", "Secondary Agent")
agent3 = orchestrator.create_agent("agent-003", "Tertiary Agent")

# Start all agents
orchestrator.start_all()

# Submit pipelines (load balanced)
pipelines = [
    {"name": "pipeline-1", "type": "etl"},
    {"name": "pipeline-2", "type": "analytics"},
    {"name": "pipeline-3", "type": "ml"},
]

for pipeline in pipelines:
    orchestrator.submit_pipeline(pipeline)

# Get status
status = orchestrator.get_status()
print(f"Orchestrator status: {status}")

# Get health
health = orchestrator.get_health()
print(f"Orchestrator health: {health}")

# Stop all agents
orchestrator.stop_all()

# ==============================================================================
# QUICK CREATE ORCHESTRATOR
# ==============================================================================

"""
Create orchestrator with multiple agents quickly:
"""

orchestrator = create_orchestrator(num_agents=5, agent_name_prefix="agent")

orchestrator.start_all()

# Submit batch of pipelines
for i in range(10):
    orchestrator.submit_pipeline({
        "name": f"batch_pipeline_{i}",
        "batch": i
    })

# Get execution history
history = orchestrator.get_execution_history(limit=5)
for execution in history:
    print(execution)

orchestrator.stop_all()

# ==============================================================================
# QUEUE MANAGEMENT
# ==============================================================================

"""
Manage pipeline queues:
"""

agent = create_hosted_agent("agent-001", "Agent with Queue")
agent.start()

# Add pipelines to queue
for i in range(5):
    agent.add_pipeline_to_queue({
        "name": f"queued_pipeline_{i}",
        "priority": i
    })

# Check queue size
queue_size = agent.get_queue_size()
print(f"Queue size: {queue_size}")

agent.stop()

# ==============================================================================
# MONITORING & HEALTH
# ==============================================================================

"""
Monitor agent health and metrics:
"""

agent = create_hosted_agent("agent-monitor", "Monitoring Agent")
agent.start()

import time

# Simulate some work
for i in range(3):
    agent.execute_pipeline({
        "name": f"test_pipeline_{i}"
    })
    time.sleep(0.1)

# Get health status
health = agent.get_health_status()
print(f"Health: {health}")
print(f"  Memory: {health['memory_mb']:.2f} MB")
print(f"  CPU: {health['cpu_percent']:.1f}%")
print(f"  Is Healthy: {health['is_healthy']}")

# Get full metrics
metrics = agent.get_metrics()
print(f"Metrics: {metrics}")

agent.stop()

# ==============================================================================
# ERROR HANDLING
# ==============================================================================

"""
Handle errors and retries:
"""

agent = create_hosted_agent(
    "agent-errors",
    "Error Handling Agent",
    max_retries=3,
    retry_delay=1
)

agent.start()

try:
    # Execute pipeline that might fail
    result = agent.execute_pipeline({
        "name": "error_pipeline",
        "config": {"fail_on_error": False}
    })
    
    if result["status"] == "failed":
        print(f"Pipeline failed: {result['error']}")
    else:
        print(f"Pipeline succeeded: {result['output']}")
        
except Exception as e:
    print(f"Execution error: {str(e)}")

finally:
    agent.stop()

# ==============================================================================
# PAUSE & RESUME
# ==============================================================================

"""
Pause and resume agent execution:
"""

agent = create_hosted_agent("agent-pause", "Pause/Resume Agent")
agent.start()

# Add pipelines
agent.add_pipeline_to_queue({"name": "pipeline-1"})
agent.add_pipeline_to_queue({"name": "pipeline-2"})

# Pause execution
agent.pause()
print(f"Agent status: {agent.get_status()}")

# Do some maintenance...

# Resume execution
agent.resume()
print(f"Agent status: {agent.get_status()}")

agent.stop()

# ==============================================================================
# JSON EXPORT
# ==============================================================================

"""
Export agent configuration and status as JSON:
"""

agent = create_hosted_agent("agent-export", "Export Agent")
agent.start()

# Get JSON representation
json_str = agent.to_json()
print(json_str)

agent.stop()

# ==============================================================================
# CLOUD INTEGRATION
# ==============================================================================

"""
Integrate with Foundry client:
"""

from src.foundry import FoundryClient

# Create Foundry client
foundry_client = FoundryClient(
    workspace_id="your-workspace",
    api_key="your-api-key"
)

# Create agent with Foundry integration
agent = create_hosted_agent(
    "agent-cloud",
    "Cloud-integrated Agent",
    foundry_client=foundry_client
)

agent.start()

# Agent can now use Foundry services
# ... submit pipelines, etc ...

agent.stop()

# ==============================================================================
# BATCH PROCESSING
# ==============================================================================

"""
Process batch of pipelines:
"""

def process_batch(agent, pipelines):
    """Process batch of pipelines"""
    results = []
    for pipeline in pipelines:
        result = agent.execute_pipeline(pipeline)
        results.append(result)
    return results

agent = create_hosted_agent("agent-batch", "Batch Processing Agent")
agent.start()

batch = [
    {"name": f"batch_item_{i}", "data": range(i*100, (i+1)*100)}
    for i in range(5)
]

results = process_batch(agent, batch)
print(f"Processed {len(results)} pipelines")

agent.stop()

# ==============================================================================
# BEST PRACTICES
# ==============================================================================

"""
Best practices when using agents:

1. Always call start() before submitting pipelines
2. Always call stop() to cleanup resources
3. Use orchestrator for multiple agents
4. Enable monitoring for production
5. Check health status regularly
6. Handle exceptions gracefully
7. Use load balancing for distribution
8. Log all important events
9. Monitor metrics and errors
10. Use with context manager for safety
"""

# Example with context manager pattern
class ManagedAgent:
    def __init__(self, config):
        self.agent = HostedAgent(config)
    
    def __enter__(self):
        self.agent.start()
        return self.agent
    
    def __exit__(self, *args):
        self.agent.stop()

# Usage
config = AgentConfig(agent_id="managed", name="Managed Agent")
with ManagedAgent(config) as agent:
    agent.add_pipeline_to_queue({"name": "pipeline"})
    print(f"Agent status: {agent.get_status()}")

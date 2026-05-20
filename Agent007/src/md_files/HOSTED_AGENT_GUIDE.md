# Microsoft Foundry - Hosted Agent

## 🎯 Overview

A **production-grade hosted agent system** for executing and orchestrating data pipelines in distributed environments. The agent framework provides:

- **Single Hosted Agent**: Execute pipelines with queue management, health monitoring, and error handling
- **Agent Orchestrator**: Manage multiple agents with load balancing and automatic coordination
- **Cloud Integration**: Native Foundry integration for cloud deployment
- **Metrics & Monitoring**: Comprehensive performance tracking and health checks

---

## 📦 Components

### **BaseAgent** (Abstract Base Class)
- Foundation for all agent implementations
- Lifecycle management (start, stop, pause, resume)
- Queue management
- Metrics collection
- Health monitoring

### **HostedAgent** (Production Implementation)
- Full-featured agent for production deployments
- Asynchronous pipeline execution
- Automatic error handling and retries
- Thread-safe operations
- System resource monitoring (CPU, memory)

### **AgentOrchestrator** (Multi-Agent Management)
- Manage multiple agents
- Load balancing across agents
- Centralized execution history
- Coordinated health monitoring
- Automatic scaling support (future)

---

## 🚀 Quick Start

### Create and Run a Single Agent

```python
from src.agents.hosted_agent import create_hosted_agent

# Create agent
agent = create_hosted_agent(
    agent_id="agent-001",
    name="Production Pipeline Agent"
)

# Start agent
agent.start()

# Submit pipeline
result = agent.execute_pipeline({
    "name": "data_pipeline",
    "module": "src.pipelines.sample_pipeline",
    "class": "SamplePipeline"
})

print(f"Result: {result}")

# Stop agent
agent.stop()
```

### Create and Run Multiple Agents

```python
from src.agents.orchestrator import create_orchestrator

# Create orchestrator with 3 agents
orchestrator = create_orchestrator(num_agents=3)

# Start all agents
orchestrator.start_all()

# Submit pipelines (load balanced automatically)
for i in range(10):
    orchestrator.submit_pipeline({
        "name": f"pipeline_{i}"
    })

# Get status
status = orchestrator.get_status()
print(f"Status: {status}")

# Stop all
orchestrator.stop_all()
```

---

## 📚 Module Structure

```
src/agents/
├── __init__.py              # Module exports
├── base_agent.py            # Abstract base class
├── hosted_agent.py          # Production agent implementation
├── orchestrator.py          # Multi-agent coordination
└── examples.py              # Usage examples
```

---

## 🔧 Configuration

### Agent Configuration

```python
from src.agents.base_agent import AgentConfig

config = AgentConfig(
    agent_id="agent-001",           # Unique identifier
    name="Production Agent",         # Human-readable name
    agent_type="hosted",            # Type of agent
    version="1.0.0",                # Agent version
    environment="production",        # Deployment environment
    max_retries=3,                  # Retry attempts
    retry_delay=5,                  # Seconds between retries
    timeout=3600,                   # Operation timeout
    enable_logging=True,            # Enable logging
    enable_monitoring=True          # Enable monitoring
)
```

### Orchestrator Configuration

```python
from src.agents.orchestrator import OrchestrationConfig

config = OrchestrationConfig(
    max_concurrent_agents=10,       # Max agents
    agent_timeout=3600,             # Agent timeout
    enable_autoscaling=False,       # Auto-scaling (future)
    enable_load_balancing=True,     # Load balancing
    health_check_interval=60        # Health check interval (seconds)
)
```

---

## 📖 Usage Examples

### Example 1: Basic Agent Usage

```python
from src.agents.hosted_agent import HostedAgent
from src.agents.base_agent import AgentConfig

# Create configuration
config = AgentConfig(
    agent_id="agent-001",
    name="Basic Agent"
)

# Create and start agent
agent = HostedAgent(config)
agent.start()

# Execute pipeline
result = agent.execute_pipeline({
    "name": "test_pipeline",
    "config": {"batch_size": 1000}
})

# Check result
print(f"Status: {result['status']}")
print(f"Execution time: {result['execution_time']}s")

# Stop agent
agent.stop()
```

### Example 2: Queue Management

```python
agent.start()

# Add multiple pipelines to queue
for i in range(5):
    agent.add_pipeline_to_queue({
        "name": f"queued_pipeline_{i}",
        "priority": i
    })

# Check queue
print(f"Queue size: {agent.get_queue_size()}")

# Pipelines execute automatically from queue
import time
time.sleep(5)

agent.stop()
```

### Example 3: Monitoring & Health

```python
agent.start()

# Execute some pipelines
agent.execute_pipeline({"name": "pipeline-1"})
agent.execute_pipeline({"name": "pipeline-2"})

# Get health status
health = agent.get_health_status()
print(f"Is Healthy: {health['is_healthy']}")
print(f"Memory: {health['memory_mb']:.2f} MB")
print(f"CPU: {health['cpu_percent']:.1f}%")

# Get metrics
metrics = agent.get_metrics()
print(f"Pipelines executed: {metrics['pipelines_executed']}")
print(f"Pipelines succeeded: {metrics['pipelines_succeeded']}")
print(f"Average execution time: {metrics['average_execution_time']:.2f}s")

agent.stop()
```

### Example 4: Using Orchestrator

```python
from src.agents.orchestrator import AgentOrchestrator, OrchestrationConfig

# Create orchestrator
config = OrchestrationConfig(enable_load_balancing=True)
orchestrator = AgentOrchestrator(config)

# Create agents
orchestrator.create_agent("agent-001", "Primary Agent")
orchestrator.create_agent("agent-002", "Secondary Agent")
orchestrator.create_agent("agent-003", "Tertiary Agent")

# Start all
orchestrator.start_all()

# Submit batch (automatically load balanced)
for i in range(10):
    orchestrator.submit_pipeline({
        "name": f"pipeline_{i}",
        "data": f"batch_{i}"
    })

# Get status
status = orchestrator.get_status()
print(f"Running agents: {status['running_agents']}")
print(f"Total pipelines: {status['total_pipelines_executed']}")

# Get health
health = orchestrator.get_health()
print(f"Overall healthy: {health['is_healthy']}")

orchestrator.stop_all()
```

### Example 5: Error Handling

```python
agent.start()

try:
    result = agent.execute_pipeline({
        "name": "error_pipeline"
    })
    
    if result["status"] == "failed":
        print(f"Error: {result['error']}")
        print(f"Execution time: {result['execution_time']}")
    else:
        print(f"Success: {result['output']}")
        
except Exception as e:
    print(f"Exception: {str(e)}")

finally:
    agent.stop()
```

---

## 🔄 Agent Lifecycle

```
┌─────────────────────┐
│   INITIALIZED       │
└──────────┬──────────┘
           │ start()
           ▼
┌─────────────────────┐
│   RUNNING           │────────────┐
└──────────┬──────────┘            │
           │                       │ pause()
           │ pause()               ▼
           ▼                   ┌─────────────────────┐
       ┌─────────────────────┐ │     PAUSED          │
       │     PAUSED          │ └──────────┬──────────┘
       └──────────┬──────────┘            │ resume()
                  │                       │
                  │ resume()              │
                  └──────────┬────────────┘
                             │
           ┌─────────────────┤
           │                 │ stop()
           ▼                 ▼
    ┌─────────────────────┐
    │   ERROR / STOPPED   │
    └─────────────────────┘
```

---

## 📊 Metrics & Monitoring

### Available Metrics

```python
metrics = agent.get_metrics()

{
    "agent_id": "agent-001",
    "status": "running",
    "pipelines_executed": 10,
    "pipelines_succeeded": 8,
    "pipelines_failed": 2,
    "total_execution_time": 45.3,
    "average_execution_time": 4.53,
    "errors_count": 3,
    "queue_size": 2,
    "last_execution_time": "2026-05-14T10:30:45.123456"
}
```

### Health Status

```python
health = agent.get_health_status()

{
    "is_healthy": true,
    "status": "running",
    "memory_mb": 142.5,
    "cpu_percent": 15.2,
    "uptime_seconds": 3600,
    "errors_count": 1,
    "queue_size": 0
}
```

---

## 🎯 Design Patterns

### Pattern 1: Single Agent

For processing pipelines with a single dedicated agent:

```python
agent = create_hosted_agent("agent-001", "Pipeline Processor")
agent.start()

# Add work
agent.add_pipeline_to_queue({"name": "pipeline"})

# Automatic processing
```

### Pattern 2: Multi-Agent Load Balancing

For distributing work across multiple agents:

```python
orchestrator = create_orchestrator(num_agents=5)
orchestrator.start_all()

# Automatically distributed
for i in range(100):
    orchestrator.submit_pipeline({"name": f"pipeline_{i}"})
```

### Pattern 3: Specialized Agents

For different types of workloads:

```python
# Create specialized agents
etl_agent = orchestrator.create_agent("etl-agent", "ETL Processing")
ml_agent = orchestrator.create_agent("ml-agent", "ML Training")
analytics_agent = orchestrator.create_agent("analytics-agent", "Analytics")

# Route specific work
orchestrator.submit_pipeline(etl_pipeline, "etl-agent")
orchestrator.submit_pipeline(ml_pipeline, "ml-agent")
orchestrator.submit_pipeline(analytics_pipeline, "analytics-agent")
```

---

## 🔗 Integration with Foundry

### With FoundryClient

```python
from src.foundry import FoundryClient
from src.agents.hosted_agent import create_hosted_agent

# Create Foundry client
foundry_client = FoundryClient(
    workspace_id="your-workspace",
    api_key="your-api-key"
)

# Create agent with Foundry integration
agent = create_hosted_agent(
    "agent-cloud",
    "Cloud Agent",
    foundry_client=foundry_client
)

agent.start()
```

### With SamplePipeline

```python
from src.pipelines.sample_pipeline import SamplePipeline
from src.agents.hosted_agent import create_hosted_agent

# Create agent
agent = create_hosted_agent("agent-pipeline", "Pipeline Agent")
agent.start()

# Submit pipeline
result = agent.execute_pipeline({
    "name": "sample_data_pipeline",
    "module": "src.pipelines.sample_pipeline",
    "class": "SamplePipeline"
})

agent.stop()
```

---

## 🛠️ Advanced Features

### Pause & Resume

```python
agent.pause()      # Pause execution
agent.resume()     # Resume execution
```

### Clear Queue

```python
agent.clear_queue()  # Remove all queued pipelines
```

### Execution History

```python
history = orchestrator.get_execution_history(limit=50)
for execution in history:
    print(f"{execution['pipeline_name']}: {execution['status']}")
```

### JSON Export

```python
json_str = agent.to_json()
print(json_str)
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
- Use `AgentOrchestrator` to manage multiple agents
- Each agent runs on separate thread
- Load balanced automatically

### Vertical Scaling
- Increase resource allocation to agent processes
- Monitor CPU and memory with health checks
- Adjust `timeout` and `max_retries` as needed

### Cloud Deployment
- Use with Azure Container Instances
- Deploy on Kubernetes with orchestrator
- Integrate with Azure Data Factory
- Monitor with Application Insights

---

## 🧪 Testing

### Unit Tests

```python
def test_agent_creation():
    agent = create_hosted_agent("test", "Test Agent")
    assert agent.config.agent_id == "test"
    assert agent.status.value == "initialized"

def test_agent_start_stop():
    agent = create_hosted_agent("test", "Test Agent")
    agent.start()
    assert agent.status.value == "running"
    agent.stop()
    assert agent.status.value == "stopped"

def test_pipeline_execution():
    agent = create_hosted_agent("test", "Test Agent")
    agent.start()
    result = agent.execute_pipeline({"name": "test"})
    assert result["status"] in ["success", "failed"]
    agent.stop()
```

---

## 🔐 Best Practices

1. **Always Stop Agents**: Call `stop()` to cleanup resources
2. **Monitor Health**: Check `get_health_status()` regularly
3. **Handle Errors**: Use try-except around submissions
4. **Use Orchestrator**: For multiple pipelines/agents
5. **Enable Logging**: Capture execution history
6. **Check Metrics**: Track performance over time
7. **Load Balance**: Let orchestrator distribute work
8. **Batch Submissions**: Submit multiple pipelines at once
9. **Review History**: Use execution history for debugging
10. **Plan Capacity**: Size agents and orchestrator appropriately

---

## 📚 Reference

### Key Classes

- `BaseAgent` - Abstract base class
- `HostedAgent` - Production agent implementation
- `AgentOrchestrator` - Multi-agent coordinator
- `AgentConfig` - Agent configuration
- `AgentStatus` - Agent lifecycle states
- `AgentMetrics` - Performance metrics

### Key Methods

**Agent Methods:**
- `start()` - Start agent
- `stop()` - Stop agent
- `execute_pipeline()` - Execute a pipeline
- `add_pipeline_to_queue()` - Queue pipeline
- `get_status()` - Get agent status
- `get_metrics()` - Get performance metrics
- `get_health_status()` - Get health information

**Orchestrator Methods:**
- `create_agent()` - Create new agent
- `get_agent()` - Get agent by ID
- `submit_pipeline()` - Submit pipeline
- `start_all()` - Start all agents
- `stop_all()` - Stop all agents
- `get_status()` - Get orchestrator status
- `get_health()` - Get health of all agents

---

## 🚀 Next Steps

1. **Review Examples**: Study `src/agents/examples.py`
2. **Run Tests**: Execute test suite
3. **Create Agents**: Deploy in your environment
4. **Monitor**: Check health and metrics
5. **Optimize**: Tune configuration based on workload
6. **Scale**: Add more agents as needed

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: May 14, 2026

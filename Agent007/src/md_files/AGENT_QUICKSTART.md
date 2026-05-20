# Hosted Agent - Quick Start Guide

## ⚡ 30-Second Setup

### 1. Create and Start an Agent

```python
from src.agents.hosted_agent import create_hosted_agent

# Create agent
agent = create_hosted_agent("my-agent", "My Agent")

# Start it
agent.start()

# Execute a pipeline
result = agent.execute_pipeline({"name": "my_pipeline"})

# Stop it
agent.stop()
```

### 2. Create a Multi-Agent Orchestrator

```python
from src.agents.orchestrator import create_orchestrator

# Create with 3 agents
orchestrator = create_orchestrator(num_agents=3)

# Start all
orchestrator.start_all()

# Submit work (automatically load balanced)
orchestrator.submit_pipeline({"name": "pipeline-1"})

# Check status
status = orchestrator.get_status()
print(f"Pipelines executed: {status['total_pipelines_executed']}")

# Stop all
orchestrator.stop_all()
```

---

## 📚 Key Classes

| Class | Purpose |
|-------|---------|
| `HostedAgent` | Single agent for pipeline execution |
| `AgentOrchestrator` | Manage multiple agents with load balancing |
| `AgentConfig` | Configuration for agents |
| `AgentStatus` | Lifecycle states |

---

## 🎯 Common Tasks

### Monitor Agent Health

```python
health = agent.get_health_status()
print(f"Memory: {health['memory_mb']:.2f} MB")
print(f"CPU: {health['cpu_percent']:.1f}%")
```

### Get Performance Metrics

```python
metrics = agent.get_metrics()
print(f"Executed: {metrics['pipelines_executed']}")
print(f"Success: {metrics['pipelines_succeeded']}")
print(f"Failed: {metrics['pipelines_failed']}")
```

### Queue Pipelines

```python
agent.add_pipeline_to_queue({"name": "queued_pipeline"})
print(f"Queue size: {agent.get_queue_size()}")
```

### Pause and Resume

```python
agent.pause()    # Stop execution (keep queued items)
agent.resume()   # Continue execution
```

---

## 🔧 Configuration

```python
from src.agents.base_agent import AgentConfig
from src.agents.hosted_agent import HostedAgent

config = AgentConfig(
    agent_id="prod-agent-001",
    name="Production Agent",
    environment="production",
    max_retries=5,
    timeout=7200,
    enable_logging=True
)

agent = HostedAgent(config)
agent.start()
```

---

## 📊 Lifecycle

```
[INITIALIZED] → start() → [RUNNING] → stop() → [STOPPED]
                            ↓
                          pause()
                            ↓
                          [PAUSED] → resume() → [RUNNING]
```

---

## ✅ Testing

Run the test suite:

```bash
pytest tests/test_agents.py -v
```

Expected output: **33 tests passed**

---

## 🚀 Next Steps

1. **Review Full Guide**: Read `HOSTED_AGENT_GUIDE.md` for complete documentation
2. **Explore Examples**: Check `src/agents/examples.py` for 50+ usage patterns
3. **Run Tests**: Execute test suite to validate your environment
4. **Deploy**: Use in production with your pipelines

---

## 💡 Tips

- Always call `stop()` when done to cleanup resources
- Use `AgentOrchestrator` for multiple concurrent pipelines
- Check `get_health_status()` regularly to monitor system
- Enable logging for debugging: `enable_logging=True` in config
- Use factory functions: `create_hosted_agent()` and `create_orchestrator()`

---

## 📖 File Locations

- **Implementation**: `src/agents/`
  - `base_agent.py` - Abstract base class
  - `hosted_agent.py` - Production agent
  - `orchestrator.py` - Multi-agent manager
  - `examples.py` - 50+ usage examples

- **Tests**: `tests/test_agents.py` (33 tests)
- **Documentation**: `HOSTED_AGENT_GUIDE.md`

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Tests**: 33 passed  
**Last Updated**: May 14, 2026

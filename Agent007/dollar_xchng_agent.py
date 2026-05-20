# Before running the sample:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from src.utils.config import load_config

# Load configuration from .env file
config = load_config()
endpoint = config.endpoint

if not endpoint:
    raise ValueError("ENDPOINT is not configured in the .env file. Please set the ENDPOINT variable.")

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "DollarCoversionAgent"
my_version = "3"

openai_client = project_client.get_openai_client()

# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Tell me what you can help with."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")




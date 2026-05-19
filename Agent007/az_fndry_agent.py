# Before running the sample:
#    pip install azure-ai-projects>=2.1.0
#    brew install azure-cli
#    az login
#    az account set --subscription <your-subscription-id>

import sys
from azure.identity import DefaultAzureCredential, AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.core.exceptions import ClientAuthenticationError

endpoint = "https://anuragkumar1973-0503-resource.services.ai.azure.com/api/projects/anuragkumar1973-0503"

# Try multiple credential types
credentials_to_try = [
    ("Azure CLI", AzureCliCredential()),
    ("DefaultAzureCredential", DefaultAzureCredential()),
]

project_client = None
for cred_name, credential in credentials_to_try:
    try:
        print(f"🔐 Attempting authentication with {cred_name}...")
        project_client = AIProjectClient(
            endpoint=endpoint,
            credential=credential,
        )
        print(f"✓ Successfully authenticated with {cred_name}")
        break
    except ClientAuthenticationError as e:
        print(f"❌ {cred_name} failed: {str(e)[:100]}...")
        continue

if project_client is None:
    print("\n" + "="*70)
    print("❌ AUTHENTICATION FAILED")
    print("="*70)
    print("\nPlease run the Azure setup script:")
    print("  bash azure-setup.sh")
    print("\nOr manually authenticate:")
    print("  1. brew install azure-cli")
    print("  2. az login")
    print("  3. az account set --subscription <your-subscription-id>")
    print("  4. python az_fndry_agent.py")
    print("\n" + "="*70 + "\n")
    sys.exit(1)

my_agent = "WeatherAlexa"
my_version = "3"

openai_client = project_client.get_openai_client()

# ============================================================================
# GET ZIP CODE FROM TERMINAL
# ============================================================================

# Method 1: Get from command line arguments
zip_code = None

# Check if zip code provided as command line argument
if len(sys.argv) > 1:
    zip_code = sys.argv[1]
    print(f"✓ Zip code from command line: {zip_code}")
else:
    # Method 2: Get from environment variable
    import os
    zip_code = os.getenv("ZIP_CODE")
    if zip_code:
        print(f"✓ Zip code from environment variable: {zip_code}")
    else:
        # Method 3: Prompt user in terminal
        print("\n" + "="*70)
        print("🌍 Enter Zip Code")
        print("="*70)
        zip_code = input("Enter a zip code to find nearby restaurants (or press Enter to skip): ").strip()
        if not zip_code:
            print("No zip code provided, using default query")
            zip_code = None

# ============================================================================
# BUILD MESSAGE FOR AGENT
# ============================================================================

if zip_code:
    user_message = f"Tell me the restaurants near this zip code {zip_code}. What can you help with?"
else:
    user_message = "Tell me what you can help with."

print(f"\n📝 Sending to agent: {user_message}\n")

# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": user_message}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")




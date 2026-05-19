"""
Azure Authentication Helper
Provides error handling and guidance for Azure authentication issues
"""

import sys
import os
from typing import Optional

def check_azure_cli() -> bool:
    """Check if Azure CLI is installed and user is logged in"""
    import subprocess
    
    try:
        result = subprocess.run(['az', 'account', 'show'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def get_credentials():
    """Get Azure credentials with error handling"""
    from azure.identity import AzureCliCredential, DefaultAzureCredential
    from azure.core.exceptions import ClientAuthenticationError
    
    # Try Azure CLI first (most common for local development)
    try:
        print("🔐 Attempting Azure CLI authentication...")
        credential = AzureCliCredential()
        # Verify it works
        credential.get_token("https://management.azure.com/.default")
        print("✓ Azure CLI authentication successful")
        return credential
    except Exception as e:
        print(f"❌ Azure CLI failed: {str(e)[:50]}...")
    
    # Try default credentials
    try:
        print("🔐 Attempting DefaultAzureCredential...")
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
        print("✓ DefaultAzureCredential successful")
        return credential
    except ClientAuthenticationError as e:
        print(f"❌ DefaultAzureCredential failed")
    
    # If we get here, authentication failed
    return None

def show_authentication_guide():
    """Show how to set up Azure authentication"""
    guide = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  ❌ AZURE AUTHENTICATION FAILED                                            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

To fix this, follow these steps:

OPTION 1: Use Azure CLI (Recommended for Local Development)
─────────────────────────────────────────────────────────────

  1. Install Azure CLI:
     brew install azure-cli

  2. Login to Azure:
     az login
     (This opens your browser for authentication)

  3. Set your subscription:
     az account set --subscription <your-subscription-id>

  4. Run the script:
     python az_fndry_agent.py

OPTION 2: Use Azure Setup Script (Automated)
──────────────────────────────────────────────

  1. Run the setup script:
     bash azure-setup.sh

  2. Follow the prompts to authenticate

  3. Run your script:
     python az_fndry_agent.py

OPTION 3: Authenticate with Service Principal (CI/CD)
──────────────────────────────────────────────────────

  1. Export environment variables:
     export AZURE_TENANT_ID="your-tenant-id"
     export AZURE_CLIENT_ID="your-client-id"
     export AZURE_CLIENT_SECRET="your-client-secret"

  2. Run the script:
     python az_fndry_agent.py

OPTION 4: Skip Azure (Test Without Credentials)
────────────────────────────────────────────────

  Run the demo instead:
    python demo.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Need help? Check these files:
  • azure-setup.sh - Automated setup script
  • SETUP_GUIDE.md - Detailed setup instructions
  • TROUBLESHOOTING.md - More troubleshooting help

For more info:
  https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot
"""
    print(guide)

if __name__ == "__main__":
    print("Azure Authentication Helper\n")
    
    if check_azure_cli():
        print("✓ Azure CLI is configured")
        credential = get_credentials()
        if credential:
            print("✓ Ready to use Azure services")
    else:
        print("❌ Azure CLI is not configured")
        show_authentication_guide()

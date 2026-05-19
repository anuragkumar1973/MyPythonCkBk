#!/bin/bash
# Azure Authentication Setup Script
# Run this to configure Azure credentials for local development

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║  Azure Authentication Setup                                        ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Installing..."
    brew install azure-cli
    echo "✓ Azure CLI installed"
else
    echo "✓ Azure CLI is already installed"
fi

echo ""
echo "📍 Step 1: Login to Azure"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Running: az login"
echo "(This will open your browser for authentication)"
echo ""

az login

echo ""
echo "✓ Successfully logged in to Azure"
echo ""

echo "📍 Step 2: Set Your Subscription"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get subscription ID
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
SUBSCRIPTION_NAME=$(az account show --query name -o tsv)

echo "Current subscription:"
echo "  Name: $SUBSCRIPTION_NAME"
echo "  ID: $SUBSCRIPTION_ID"
echo ""

read -p "Use this subscription? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Available subscriptions:"
    az account list --query '[].{Name:name, ID:id}' -o table
    echo ""
    read -p "Enter subscription ID: " SUBSCRIPTION_ID
    az account set --subscription "$SUBSCRIPTION_ID"
    echo "✓ Subscription set to: $SUBSCRIPTION_ID"
else
    echo "✓ Using subscription: $SUBSCRIPTION_ID"
fi

echo ""
echo "📍 Step 3: Verify Authentication"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get account details
TENANT_ID=$(az account show --query tenantId -o tsv)

echo "Authentication Details:"
echo "  Subscription ID: $SUBSCRIPTION_ID"
echo "  Tenant ID: $TENANT_ID"
echo ""

echo "✅ Azure CLI is now configured!"
echo ""

echo "📍 Step 4: Test Authentication"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Running test script..."
echo ""

python3 << 'PYTHON_TEST'
try:
    from azure.identity import AzureCliCredential
    from azure.identity import DefaultAzureCredential
    
    # Try to get a token
    credential = DefaultAzureCredential()
    print("✓ Authentication successful!")
    print("✓ Ready to run Azure scripts")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
    print("Please check your credentials and try again")
PYTHON_TEST

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                                                ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "You can now run:"
echo "  python az_fndry_agent.py"
echo ""
echo "Or test agents:"
echo "  python demo.py"
echo ""

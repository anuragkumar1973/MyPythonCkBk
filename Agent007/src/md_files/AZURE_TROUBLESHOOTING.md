# Azure Authentication Troubleshooting Guide

## 🔴 Error: `DefaultAzureCredential failed to retrieve a token`

This error means Azure can't authenticate with any of the available methods.

---

## ✅ Solutions (Try in Order)

### **Solution 1: Azure CLI (Recommended)**

This is the easiest and most common method for local development.

**Steps:**

```bash
# 1. Install Azure CLI
brew install azure-cli

# 2. Login to Azure (opens browser)
az login

# 3. Set your subscription
az account set --subscription <your-subscription-id>

# 4. Verify it works
az account show

# 5. Run your script
python az_fndry_agent.py
```

**Expected Output:**
```
✓ Azure CLI authentication successful
✓ Ready to use Azure services
```

---

### **Solution 2: Use the Automated Setup Script**

```bash
# Run the setup script
bash azure-setup.sh

# Follow the prompts
# Run your script
python az_fndry_agent.py
```

---

### **Solution 3: Environment Variables (for CI/CD)**

If you can't use Azure CLI (e.g., in GitHub Actions), use environment variables.

**Steps:**

1. **Get your credentials:**
   ```bash
   # Subscription ID
   az account show --query id -o tsv
   
   # Tenant ID
   az account show --query tenantId -o tsv
   ```

2. **Create a service principal** (if you don't have one):
   ```bash
   az ad sp create-for-rbac \
     --name "MyAppServicePrincipal" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}
   ```
   
   This will output:
   ```json
   {
     "appId": "your-client-id",
     "password": "your-client-secret",
     "tenant": "your-tenant-id"
   }
   ```

3. **Add to your `.env` file:**
   ```
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret
   ```

4. **Or export as environment variables:**
   ```bash
   export AZURE_TENANT_ID="your-tenant-id"
   export AZURE_CLIENT_ID="your-client-id"
   export AZURE_CLIENT_SECRET="your-client-secret"
   python az_fndry_agent.py
   ```

---

### **Solution 4: Skip Azure (Test Without Authentication)**

If you don't need Azure yet:

```bash
# Run the demo instead
python demo.py

# Or run tests
pytest tests/ -v
```

---

## 🔧 Diagnostics

### **Check if Azure CLI is installed:**
```bash
which az
az --version
```

### **Check if you're logged in:**
```bash
az account show
```

### **Check your current subscription:**
```bash
az account list
az account set --subscription <subscription-id>
```

### **Test Python Azure libraries:**
```bash
python3 << 'EOF'
try:
    from azure.identity import AzureCliCredential
    from azure.identity import DefaultAzureCredential
    credential = DefaultAzureCredential()
    print("✓ Azure libraries are working")
except Exception as e:
    print(f"❌ Error: {e}")
EOF
```

---

## 📍 Which Method to Use?

| Situation | Method | Difficulty |
|-----------|--------|-----------|
| **Local development** | Azure CLI | Easy ⭐ |
| **GitHub Actions / CI/CD** | Environment Variables | Medium ⭐⭐ |
| **Automated setup** | azure-setup.sh | Easy ⭐ |
| **Quick test** | Skip Azure / demo.py | Easy ⭐ |

---

## 🔑 Azure CLI Quick Reference

```bash
# Login
az login

# Show current account
az account show

# List all subscriptions
az account list

# Set subscription
az account set --subscription <subscription-id>

# Get subscription ID
az account show --query id -o tsv

# Get tenant ID
az account show --query tenantId -o tsv

# Logout
az logout
```

---

## ❓ Common Issues

### **Issue: "Azure CLI not found on path"**
```bash
# Install Azure CLI
brew install azure-cli

# Add to PATH (if not already)
export PATH="/opt/homebrew/bin:$PATH"
```

### **Issue: "No accounts were found in the cache"**
```bash
# Run login again
az login
```

### **Issue: "Subscription not set"**
```bash
# Set your subscription
az account set --subscription <your-subscription-id>
```

### **Issue: "Python can't find azure libraries"**
```bash
# Install Azure Python packages
pip install azure-identity azure-ai-projects azure-core
```

---

## 📞 Support

For more help:
- Microsoft docs: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot
- Azure CLI: https://docs.microsoft.com/cli/azure/
- File: `SETUP_GUIDE.md` in this project

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Azure CLI is installed: `az --version`
- [ ] You're logged in: `az account show` (shows your account)
- [ ] Subscription is set: `az account list` (shows current marked with `isDefault`)
- [ ] Python can authenticate: Run `azure_auth_helper.py`
- [ ] Script runs: `python az_fndry_agent.py`

If any step fails, run `bash azure-setup.sh` to start over.

---

**Last Updated:** May 14, 2026

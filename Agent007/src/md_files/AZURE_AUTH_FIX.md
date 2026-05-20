# Azure Authentication Error - Complete Solution Guide

## 🔴 Problem Summary

You got this error when running `python az_fndry_agent.py`:

```
azure.core.exceptions.ClientAuthenticationError: 
DefaultAzureCredential failed to retrieve a token from the included credentials.
```

**Root Cause:** Azure SDK couldn't find any valid authentication credentials.

---

## ✅ Complete Solution

### **Step 1: Install Azure CLI** (1 minute)

```bash
brew install azure-cli
```

Verify:
```bash
az --version
```

### **Step 2: Authenticate with Azure** (2 minutes)

```bash
az login
```

This opens your browser. Sign in with your Azure account.

### **Step 3: Set Your Subscription** (1 minute)

```bash
# Find your subscription ID
az account list

# Set it
az account set --subscription <your-subscription-id>

# Verify
az account show
```

### **Step 4: Test** (1 minute)

```bash
python azure_auth_helper.py
```

Should show:
```
✓ Azure CLI is configured
✓ Ready to use Azure services
```

### **Step 5: Run Your Script** (1 minute)

```bash
python az_fndry_agent.py
```

Done! 🎉

---

## 🔧 Alternative: Automated Setup

If you want everything automated:

```bash
bash azure-setup.sh
```

This script does steps 1-4 automatically.

---

## 📁 New Files Created

| File | Purpose |
|------|---------|
| `azure-setup.sh` | Automated setup (recommended) |
| `azure_auth_helper.py` | Test authentication |
| `AZURE_TROUBLESHOOTING.md` | Detailed troubleshooting |
| `az_fndry_agent.py` | Updated with better error messages |

---

## 🎯 How It Works

**Before:** Your script tried to use `DefaultAzureCredential()` but had no credentials configured.

**Now:** 
1. Azure CLI stores credentials locally after `az login`
2. Your script uses those credentials automatically
3. If that fails, you get helpful error messages

---

## ⚠️ Common Issues

### "Azure CLI not found"
```bash
brew install azure-cli
```

### "No accounts in cache"
```bash
az login
```

### "Subscription not set"
```bash
az account set --subscription <your-subscription-id>
```

### "Still doesn't work?"
1. Check: `az account show`
2. Check: `python azure_auth_helper.py`
3. Read: `AZURE_TROUBLESHOOTING.md`

---

## 💡 Key Concepts

**What is DefaultAzureCredential?**
- Tries multiple authentication methods in order
- Checks: Environment variables, Azure CLI, Managed Identity, etc.
- Fails if none work

**What is Azure CLI?**
- Command-line tool to manage Azure resources
- Stores your credentials securely after `az login`
- Most common way to authenticate locally

**What is a Subscription?**
- Your billing account in Azure
- Each user/organization has one or more
- You must set which one to use

---

## 📞 Need More Help?

1. **Check status:**
   ```bash
   az account show
   python azure_auth_helper.py
   ```

2. **Read detailed guide:**
   ```bash
   cat AZURE_TROUBLESHOOTING.md
   ```

3. **Microsoft docs:**
   - DefaultAzureCredential: https://aka.ms/azsdk/python/identity/defaultazurecredential/troubleshoot
   - Azure CLI: https://docs.microsoft.com/cli/azure/

---

## ✅ Verification Checklist

Before running your script, verify:

- [ ] Azure CLI installed: `az --version`
- [ ] Logged in: `az account show` (shows your account)
- [ ] Subscription set: See "isDefault: true" in `az account list`
- [ ] Python can authenticate: `python azure_auth_helper.py` shows "✓"
- [ ] Script runs: `python az_fndry_agent.py` works

---

## 🚀 Quick Start

**Fastest way to fix (1 command):**
```bash
bash azure-setup.sh
```

**Then run:**
```bash
python az_fndry_agent.py
```

Done! 🎉

---

**Last Updated:** May 14, 2026  
**Status:** ✅ FIXED

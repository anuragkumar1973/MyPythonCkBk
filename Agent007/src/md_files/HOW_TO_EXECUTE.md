# 🚀 How to Execute the Entire Agent007 Project

Complete guide to running the Microsoft Foundry Multi-Agent Architecture project.

---

## 📋 Prerequisites

Before executing, make sure you have:

```bash
✓ Python 3.9+ installed
✓ Virtual environment activated
✓ Dependencies installed
✓ .env file configured
```

### Quick Check

```bash
python --version                    # Should show 3.9+
source venv/bin/activate           # Activate virtual environment
pip list | grep -E "azure|pyspark" # Check key packages
```

---

## 🎯 Execution Methods

Choose based on your needs:

### **Method 1: Quick Demo (Recommended First Step) ⭐**

**No Java required! No Spark! Just Python!**

```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
python demo.py
```

**What it does:**
- ✅ Loads configuration from `.env` file
- ✅ Displays Azure credentials (Subscription, Resource Group, Storage Account)
- ✅ Shows all project settings
- ✅ Verifies everything is configured correctly
- ✅ Takes ~2 seconds to run

**Expected Output:**
```
======================================================================
AZURE CREDENTIALS FROM .env FILE
======================================================================
Subscription ID:    12345678-1234-1234-1234-123456789012
Resource Group:     my-resource-group
Storage Account:    mystorageaccount
======================================================================

======================================================================
APPLICATION CONFIGURATION
======================================================================
Environment: development
Log Level: INFO
Debug Mode: True
...
```

---

### **Method 2: Run Tests**

**Verify everything is working correctly with 33 tests**

```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
pytest tests/ -v
```

**Individual test suites:**

```bash
# Test agents only
pytest tests/test_agents.py -v

# Test transforms only
pytest tests/test_transforms.py -v

# Test with coverage report
pytest tests/ -v --cov=src
```

**Expected Output:**
```
tests/test_agents.py::test_agent_config ✓
tests/test_agents.py::test_hosted_agent_creation ✓
tests/test_agents.py::test_agent_lifecycle ✓
...
======================== 33 passed in 2.45s ========================
```

---

### **Method 3: Run Azure Foundry Agent**

**Query Azure AI with zip code input**

```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
python az_fndry_agent.py
```

**Three ways to provide input:**

#### **Option A: Command-line argument**
```bash
python az_fndry_agent.py 10001
# Result: Queries restaurants near New York (10001)
```

#### **Option B: Environment variable**
```bash
export ZIP_CODE=90210
python az_fndry_agent.py
# Result: Queries restaurants near Los Angeles (90210)
```

#### **Option C: Interactive prompt**
```bash
python az_fndry_agent.py
# You'll be prompted: "Enter a zip code: "
# Type: 60601
# Result: Queries restaurants near Chicago (60601)
```

---

### **Method 4: Full Pipeline (Requires Java)**

**Advanced: Complete data engineering pipeline with Spark**

#### Prerequisites:
```bash
# Install Java (required for Spark)
brew install openjdk@11

# Configure JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

#### Run:
```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
python run_pipeline.py
```

**What it does:**
- ✅ Loads raw data from `data/raw/`
- ✅ Executes Spark transformations
- ✅ Saves processed data to `data/processed/`
- ✅ Generates checkpoints
- ✅ Logs all operations

---

### **Method 5: Use the Quickstart Script**

**All-in-one setup and info script**

```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
bash quickstart.sh
```

**What it does:**
- ✅ Activates virtual environment
- ✅ Shows all available commands
- ✅ Displays documentation locations
- ✅ Suggests next steps

---

## 📊 Complete Execution Workflow

### **Day 1: Get Started**

```bash
# Step 1: Activate environment
source venv/bin/activate

# Step 2: Run quick demo
python demo.py

# Step 3: Run tests
pytest tests/ -v

# Step 4: Check configuration
cat .env

# Step 5: Read documentation
open README.md
```

### **Day 2: Try the Agent**

```bash
# Step 1: Activate environment
source venv/bin/activate

# Step 2: Run Azure agent without arguments
python az_fndry_agent.py

# Step 3: Run with zip code
python az_fndry_agent.py 10001

# Step 4: Try environment variable
export ZIP_CODE=90210
python az_fndry_agent.py
```

### **Day 3: Full Pipeline (Advanced)**

```bash
# Step 1: Install Java
brew install openjdk@11

# Step 2: Set JAVA_HOME
export JAVA_HOME=$(/usr/libexec/java_home -v 11)

# Step 3: Run full pipeline
python run_pipeline.py
```

---

## 🔧 Execution Command Reference

| Task | Command | Time | Requires |
|------|---------|------|----------|
| Quick Demo | `python demo.py` | 2 sec | Python |
| Run All Tests | `pytest tests/ -v` | 5 sec | Python, pytest |
| Run Agent | `python az_fndry_agent.py 10001` | 3 sec | Python, Azure CLI |
| Run Pipeline | `python run_pipeline.py` | 30 sec | Python, Java, Spark |
| Show Help | `bash quickstart.sh` | 1 sec | Bash |
| Show Config | `cat .env` | 1 sec | None |

---

## 🚨 Troubleshooting

### **Issue: "No module named 'src'"**
**Solution:**
```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
python -c "import sys; print(sys.path)"
```

### **Issue: "Azure credentials not found"**
**Solution:**
```bash
# Check .env file
cat .env

# Set credentials manually
export AZURE_SUBSCRIPTION_ID="your-id"
export AZURE_RESOURCE_GROUP="your-group"
export AZURE_STORAGE_ACCOUNT="your-account"

# Run demo
python demo.py
```

### **Issue: "JAVA_HOME not set"**
**Solution:**
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
echo $JAVA_HOME  # Verify it's set
```

### **Issue: "ModuleNotFoundError: No module named 'pyspark'"**
**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📈 Performance & Output

### Demo Output Size
- **Time**: ~2 seconds
- **Output**: ~200 lines
- **CPU**: Minimal (<5%)
- **Memory**: Minimal (<50 MB)

### Tests Output Size
- **Time**: ~5 seconds
- **Output**: ~50 lines (33 test results)
- **CPU**: ~20%
- **Memory**: ~100 MB

### Azure Agent Output Size
- **Time**: ~3 seconds
- **Output**: ~100 lines (depends on API response)
- **CPU**: ~10%
- **Memory**: ~80 MB

### Full Pipeline Output Size
- **Time**: ~30 seconds
- **Output**: ~500 lines
- **CPU**: ~80%
- **Memory**: ~500 MB (depends on data size)

---

## 🎯 Recommended Execution Order

**For New Users:**
1. ✅ `python demo.py` - See it works
2. ✅ `pytest tests/ -v` - Verify tests pass
3. ✅ `python az_fndry_agent.py 10001` - Try the agent
4. 📖 Read documentation
5. 🔧 Install Java for full pipeline

**For Advanced Users:**
1. ✅ Skip to `python run_pipeline.py`
2. ✅ Create custom transforms
3. ✅ Modify pipelines
4. ✅ Deploy to cloud

---

## 📚 Related Documentation

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Detailed setup
- **AGENT_QUICKSTART.md** - Agent quick start
- **AGENT_ZIP_CODE_GUIDE.md** - Zip code feature guide
- **HOSTED_AGENT_GUIDE.md** - Complete agent reference
- **AZURE_AUTH_FIX.md** - Azure setup help
- **TROUBLESHOOTING.md** - Common issues

---

## ✅ Success Indicators

**Demo works if you see:**
```
✓ Configuration loaded successfully!
✓ Azure credentials are configured and ready!
```

**Tests work if you see:**
```
======================== 33 passed ========================
```

**Agent works if you see:**
```
Response output: [JSON response from Azure AI]
```

**Pipeline works if you see:**
```
✓ Pipeline completed successfully!
Data saved to: data/processed/
```

---

## 🎉 You're Ready!

You now have multiple ways to execute the Agent007 project depending on your needs:

- **Quick check?** → `python demo.py`
- **Verify quality?** → `pytest tests/ -v`
- **Try the agent?** → `python az_fndry_agent.py 10001`
- **Full processing?** → `python run_pipeline.py`

**Pick any method above and start executing!** 🚀

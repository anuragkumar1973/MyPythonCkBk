# Microsoft Foundry Project - Troubleshooting Guide

## 🔧 Common Issues and Solutions

### 1. ❌ `ModuleNotFoundError: No module named 'src'`

**Problem**: Python can't find the project modules

**Solution**:
```bash
# Method 1: Use run_pipeline.py (recommended)
python run_pipeline.py

# Method 2: Set PYTHONPATH
export PYTHONPATH=/Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
python src/pipelines/sample_pipeline.py

# Method 3: Run from project root
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
python -m src.pipelines.sample_pipeline
```

### 2. ❌ `pyspark.errors.exceptions.base.PySparkRuntimeError: [JAVA_GATEWAY_EXITED]`

**Problem**: Java is not installed

**Solution**:
```bash
# Install Java (macOS)
brew install openjdk@11

# Verify installation
java -version

# Then run pipeline
python run_pipeline.py
```

### 3. ❌ `pydantic.errors.PydanticImportError: BaseSettings has been moved`

**Problem**: pydantic-settings not installed

**Solution**:
```bash
# Install pydantic-settings
pip install pydantic-settings

# Verify
pip list | grep pydantic
```

### 4. ❌ Virtual environment not activated

**Problem**: Commands fail with "module not found" errors

**Solution**:
```bash
# Activate venv
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
source venv/bin/activate

# Check activation (should show (venv) in prompt)
echo $VIRTUAL_ENV
```

### 5. ❌ Configuration error: Extra fields not permitted

**Problem**: `.env` file has fields not in Config model

**Solution**:
- Already fixed in config.py with `extra = "ignore"`
- The .env file can have any fields; only defined ones are used

### 6. ❌ Import errors in IDE (VS Code)

**Problem**: VS Code shows "Import not found" errors

**Solution**:
```bash
# Open VS Code from project root
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
code .

# VS Code should auto-detect venv in .vscode/settings.json
# If not, set Python interpreter manually:
# Cmd+Shift+P → Python: Select Interpreter → ./venv/bin/python
```

## ✅ Verification Checklist

Run this to verify everything is working:

```bash
# 1. Activate environment
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
source venv/bin/activate

# 2. Check Python
python --version  # Should be 3.13.x

# 3. Check packages
pip list | grep -E "pyspark|pydantic|azure-"

# 4. Run demo (no Java required)
python demo.py

# 5. Run tests
pytest tests/ -v

# 6. Check configuration
python -c "from src.utils.config import load_config; c = load_config(); print(f'Config loaded: {c.environment}')"
```

## 🚀 Getting Started Again

If you need a fresh start:

```bash
# 1. Navigate to project
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007

# 2. Activate environment (or create new)
source venv/bin/activate
# OR
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run demo
python demo.py

# 5. Create .env
cp config/example.env .env
nano .env  # Add your credentials

# 6. Run full pipeline (requires Java)
python run_pipeline.py
```

## 📊 Project Structure Verification

Verify all required files exist:

```bash
# Check core files
ls -la src/__init__.py
ls -la src/foundry/__init__.py
ls -la src/pipelines/sample_pipeline.py
ls -la src/transforms/base.py
ls -la src/utils/config.py
ls -la src/utils/logger.py

# Check config files
ls -la config/example.env
ls -la config/pipeline.yml
ls -la .env  # Should exist after setup

# Check test files
ls -la tests/__init__.py
ls -la tests/test_transforms.py

# Check scripts
ls -la demo.py
ls -la run_pipeline.py
```

## 🔐 Environment Variable Setup

If .env file is not working:

```bash
# Export manually
export ENVIRONMENT=development
export LOG_LEVEL=INFO
export FOUNDRY_WORKSPACE=your-workspace
export FOUNDRY_API_KEY=your-api-key
export AZURE_SUBSCRIPTION_ID=your-id
export AZURE_RESOURCE_GROUP=your-group

# Then run
python demo.py
```

## 🧪 Testing the Project

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_transforms.py::test_cleaning_transform_removes_duplicates -v

# Generate coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

## 🐛 Debug Mode

Enable debug logging:

```bash
# Method 1: Edit .env
echo "LOG_LEVEL=DEBUG" >> .env

# Method 2: Run with debug flag
LOG_LEVEL=DEBUG python demo.py

# Method 3: In code
from src.utils.logger import set_log_level, get_logger
logger = get_logger(__name__)
set_log_level(logger, "DEBUG")
```

## 📞 Quick Support

| Issue | Quick Fix |
|-------|-----------|
| Module not found | Use `python run_pipeline.py` instead |
| Java missing | `brew install openjdk@11` |
| pydantic-settings missing | `pip install pydantic-settings` |
| venv not activated | `source venv/bin/activate` |
| Configuration error | Run `python demo.py` to test config loading |
| Import errors in IDE | Reload VS Code window (Cmd+Shift+P → Reload Window) |

## 🎓 Learning Resources

- **Python**: https://www.python.org/
- **PySpark**: https://spark.apache.org/docs/latest/api/python/
- **Pydantic**: https://docs.pydantic.dev/
- **Azure SDK**: https://learn.microsoft.com/en-us/python/azure/

## 📝 Notes

- Project requires Python 3.9+
- Spark requires Java 8 or 11
- All credentials should be in .env (never commit)
- Use `-v` flag with pytest for verbose output
- JSON logging format can be parsed by Azure Log Analytics

---

**Still stuck?** Check the error message carefully - it usually points to the fix!

Happy coding! 🚀

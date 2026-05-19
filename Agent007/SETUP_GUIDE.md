# Microsoft Foundry Project - Setup Guide

## ✅ Project Created Successfully!

Your Microsoft Foundry project has been scaffolded and is ready for development.

### 📋 What's Been Done

✅ **Project Structure Created**
- `src/foundry/` - Foundry client integration
- `src/pipelines/` - Sample pipeline implementation
- `src/transforms/` - Data transformation components
- `src/utils/` - Logging and configuration utilities
- `tests/` - Unit test examples
- `config/` - Configuration files
- `data/` - Data directories (raw, processed)

✅ **Dependencies Installed**
- PySpark 3.5.1 - Distributed data processing
- Azure SDK - Cloud integration
- Pydantic - Configuration management
- Pytest - Testing framework
- Structlog - Structured logging

✅ **Python Virtual Environment**
- Location: `./venv/`
- Python: 3.13.7
- Packages: 35+ installed

### 🚀 Next Steps

#### 1. Activate Virtual Environment

```bash
cd /Users/anuragkumar1973/Downloads/book_py_cookbk/Agent007
source venv/bin/activate
```

#### 2. Configure Environment

```bash
# Copy example environment file
cp config/example.env .env

# Edit .env with your Azure credentials
nano .env
```

Example `.env` configuration:
```env
ENVIRONMENT=development
LOG_LEVEL=INFO
DEBUG=False

AZURE_SUBSCRIPTION_ID=your-subscription-id
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_STORAGE_ACCOUNT=your-storage-account

FOUNDRY_WORKSPACE=your-workspace
FOUNDRY_API_KEY=your-api-key
```

#### 3. Run Sample Pipeline

```bash
python src/pipelines/sample_pipeline.py
```

Expected output:
```
🔄 Initializing Azure AI Project Client...
✓ Azure AI Project Client initialized successfully!

Executing cleaning
Completed cleaning: 5 rows
...
```

#### 4. Run Tests

```bash
pytest tests/ -v --cov=src
```

#### 5. View Project Structure

```bash
tree src/ -I '__pycache__'
```

### 📚 Project Components

#### Foundry Client (`src/foundry/client.py`)
Central integration point for Microsoft Foundry operations:
- Spark session management
- Configuration handling
- API authentication

#### Transforms (`src/transforms/`)
Reusable data transformation components:
- `BaseTransform` - Abstract base class
- `CleaningTransform` - Data cleaning
- `FilterTransform` - Conditional filtering
- `AggregationTransform` - Data aggregation

#### Pipeline (`src/pipelines/sample_pipeline.py`)
Example data pipeline showing:
- Data creation
- Transform application
- Error handling
- Logging

#### Utilities (`src/utils/`)
- `logger.py` - Structured JSON logging
- `config.py` - Configuration management with Pydantic

### 🔧 Development Workflow

#### Adding a New Transform

```python
from src.transforms import BaseTransform

class MyTransform(BaseTransform):
    def transform(self, df):
        # Your transformation logic
        return df.filter(...)
```

#### Adding a New Pipeline

```python
from src.pipelines import SamplePipeline
from src.foundry import FoundryClient

class MyPipeline(SamplePipeline):
    def run(self):
        # Your pipeline logic
        pass
```

#### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
pylint src/

# Type checking
mypy src/

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html
```

### 🔐 Security Best Practices

1. ✅ **Never commit `.env`** - Add to `.gitignore` (already done)
2. ✅ **Use environment variables** - Config loads from `.env`
3. ✅ **Managed identities** - Use Azure MSI for authentication
4. ✅ **Structured logging** - JSON format for audit trails
5. ✅ **Data isolation** - Raw and processed data separated

### 📊 Configuration

#### Development Environment (`config/example.env`)
```env
ENVIRONMENT=development
SPARK_MASTER=local[*]
LOG_LEVEL=DEBUG
```

#### Production Environment
```env
ENVIRONMENT=production
SPARK_MASTER=yarn
LOG_LEVEL=INFO
```

### 🧪 Testing

Unit tests are in `tests/`:
- `test_transforms.py` - Transform tests

Run tests:
```bash
pytest tests/ -v
pytest tests/test_transforms.py::test_cleaning_transform_removes_duplicates -v
pytest tests/ --cov=src --cov-report=html
```

### 📖 Documentation

- **README.md** - Project overview and quick start
- **copilot-instructions.md** - Development guidelines
- **pipeline.yml** - Pipeline configuration
- **Inline comments** - Code documentation

### 🆘 Troubleshooting

#### Spark not found
```bash
export SPARK_HOME=/usr/local/Cellar/apache-spark/3.5.1
export PATH=$PATH:$SPARK_HOME/bin
```

#### Memory errors
Edit `.env`:
```env
SPARK_DRIVER_MEMORY=8g
SPARK_EXECUTOR_MEMORY=4g
```

#### Azure authentication fails
```bash
az login
az account set --subscription <subscription-id>
```

### 🎯 Key Files

| File | Purpose |
|------|---------|
| `src/__init__.py` | Package initialization |
| `src/foundry/client.py` | Foundry integration |
| `src/pipelines/sample_pipeline.py` | Example pipeline |
| `src/transforms/base.py` | Transform base classes |
| `src/utils/config.py` | Configuration management |
| `src/utils/logger.py` | Logging utilities |
| `config/example.env` | Environment template |
| `requirements.txt` | Python dependencies |
| `tests/test_transforms.py` | Unit tests |

### 🚀 Quick Commands

```bash
# Activate environment
source venv/bin/activate

# Run pipeline
python src/pipelines/sample_pipeline.py

# Run tests
pytest tests/ -v

# Format code
black src/

# Check coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### 📞 Support

For issues and questions:
1. Check README.md for detailed documentation
2. Review code examples in `src/pipelines/`
3. Run tests to validate setup
4. Check logs for error messages

### 🎉 Ready to Start!

Your Microsoft Foundry project is configured and ready. Start by:

1. ✅ Activating the virtual environment
2. ✅ Configuring `.env` with your settings
3. ✅ Running the sample pipeline
4. ✅ Creating your first transform
5. ✅ Building your data pipeline

Happy coding! 🚀

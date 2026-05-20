# Microsoft Foundry - Model Catalog

## 📋 Overview

This document provides a comprehensive catalog of all components, models, and patterns available in the Microsoft Foundry project. Use this as a reference guide for developing data pipelines and transformations.

---

## 🏗️ Core Framework Components

### 1. **FoundryClient** 
**Location**: `src/foundry/__init__.py`

**Purpose**: Central integration point for Microsoft Foundry operations and Spark session management.

**Class**: `FoundryClient`

**Key Methods**:
- `__init__()` - Initialize with workspace ID and API key
- `_create_spark_session()` - Create configured Spark session
- `get_spark_session()` - Get active Spark session
- `get_config()` - Retrieve configuration values
- `close()` - Close Spark session

**Usage Example**:
```python
from src.foundry import FoundryClient
from src.utils.config import load_config

config = load_config()
client = FoundryClient(
    workspace_id=config.foundry_workspace,
    api_key=config.foundry_api_key,
    config=config.to_dict()
)

spark = client.get_spark_session()
# Use spark for data operations
client.close()
```

**Attributes**:
- `workspace_id` (str) - Foundry workspace identifier
- `api_key` (str) - API authentication key
- `config` (dict) - Configuration dictionary
- `spark_session` (SparkSession) - Active Spark session
- `logger` - Logger instance

---

## 🔄 Data Transform Components

### Base Transform Class
**Location**: `src/transforms/base.py`

**Class**: `BaseTransform` (Abstract)

**Purpose**: Abstract base class for all custom transformations.

**Abstract Methods**:
- `transform(df: DataFrame) -> DataFrame` - Implement transformation logic

**Inherited Methods**:
- `validate_input(df, required_columns)` - Validate required columns
- `__call__(df)` - Make transform callable

**Usage Example**:
```python
from src.transforms import BaseTransform
from pyspark.sql import DataFrame

class CustomTransform(BaseTransform):
    def transform(self, df: DataFrame) -> DataFrame:
        return df.filter(df.age > 18)

# Use it
transform = CustomTransform("adult_filter")
result = transform(input_df)
```

---

### 2. **CleaningTransform**
**Location**: `src/transforms/base.py`

**Purpose**: Remove duplicates and null values

**Class**: `CleaningTransform(BaseTransform)`

**Methods**:
- `transform(df)` - Remove duplicates and all-null rows

**Usage**:
```python
from src.transforms import CleaningTransform

cleaning = CleaningTransform("data_cleaning")
clean_df = cleaning(raw_df)
```

**Operations**:
- Drops duplicate rows
- Removes rows with all null values

---

### 3. **FilterTransform**
**Location**: `src/transforms/base.py`

**Purpose**: Apply conditional filters to data

**Class**: `FilterTransform(BaseTransform)`

**Configuration**:
```python
config = {
    "condition": "salary > 50000 AND age < 65"
}
```

**Usage**:
```python
from src.transforms import FilterTransform

filter_config = {"condition": "status == 'active'"}
filter_transform = FilterTransform("status_filter", config=filter_config)
filtered_df = filter_transform(input_df)
```

**Supported Operations**:
- Comparison: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Logical: `AND`, `OR`, `NOT`
- String functions: `like`, `rlike`

---

### 4. **AggregationTransform**
**Location**: `src/transforms/base.py`

**Purpose**: Aggregate data using groupBy and aggregate functions

**Class**: `AggregationTransform(BaseTransform)`

**Configuration**:
```python
config = {
    "group_by": ["department", "year"],
    "aggregations": {
        "salary": "avg",
        "count": "count"
    }
}
```

**Usage**:
```python
from src.transforms import AggregationTransform
from pyspark.sql.functions import avg, sum, count

config = {
    "group_by": ["dept"],
    "aggregations": {
        "salary": avg("salary"),
        "headcount": count("*")
    }
}
agg_transform = AggregationTransform("dept_summary", config=config)
result = agg_transform(input_df)
```

**Supported Functions**:
- `sum()` - Sum aggregation
- `avg()` - Average aggregation
- `count()` - Count aggregation
- `min()` - Minimum value
- `max()` - Maximum value
- `stddev()` - Standard deviation
- `collect_list()` - Collect values in list

---

## 🔧 Utility Components

### Configuration Management
**Location**: `src/utils/config.py`

**Class**: `Config(BaseSettings)`

**Purpose**: Pydantic-based configuration management with environment variable support

**Configuration Fields**:

| Field | Type | Default | Environment Variable |
|-------|------|---------|----------------------|
| environment | str | "development" | ENVIRONMENT |
| log_level | str | "INFO" | LOG_LEVEL |
| debug | bool | False | DEBUG |
| azure_subscription_id | Optional[str] | None | AZURE_SUBSCRIPTION_ID |
| azure_resource_group | Optional[str] | None | AZURE_RESOURCE_GROUP |
| azure_storage_account | Optional[str] | None | AZURE_STORAGE_ACCOUNT |
| azure_storage_key | Optional[str] | None | AZURE_STORAGE_KEY |
| foundry_workspace | Optional[str] | None | FOUNDRY_WORKSPACE |
| foundry_api_key | Optional[str] | None | FOUNDRY_API_KEY |
| spark_master | str | "local[*]" | SPARK_MASTER |
| spark_driver_memory | str | "4g" | SPARK_DRIVER_MEMORY |
| spark_executor_memory | str | "2g" | SPARK_EXECUTOR_MEMORY |
| data_raw_path | str | "./data/raw" | DATA_RAW_PATH |
| data_processed_path | str | "./data/processed" | DATA_PROCESSED_PATH |
| checkpoint_path | str | "./checkpoints" | CHECKPOINT_PATH |
| batch_size | int | 1000 | BATCH_SIZE |
| max_retries | int | 3 | MAX_RETRIES |
| retry_delay | int | 5 | RETRY_DELAY |
| timeout | int | 3600 | TIMEOUT |

**Usage**:
```python
from src.utils.config import load_config

# Load from .env file
config = load_config()

# Access configuration
print(config.environment)  # "development"
print(config.batch_size)  # 1000

# Get with default
value = config.get("custom_key", "default")

# Convert to dict
config_dict = config.to_dict()
```

**Methods**:
- `load_config()` - Load configuration from .env
- `from_yaml(yaml_path)` - Load from YAML file
- `to_dict()` - Convert to dictionary
- `get(key, default)` - Get value with default

---

### Logging
**Location**: `src/utils/logger.py`

**Class**: `JSONFormatter(logging.Formatter)`

**Purpose**: Format logs as JSON for structured logging

**Function**: `get_logger(name, level=None)`

**Returns**: Configured logger instance

**Log Output Format**:
```json
{
    "timestamp": "2026-05-14T10:30:45.123456",
    "level": "INFO",
    "logger": "module_name",
    "message": "Your log message",
    "module": "sample.py",
    "function": "main",
    "line": 42
}
```

**Usage**:
```python
from src.utils.logger import get_logger, set_log_level

# Create logger
logger = get_logger(__name__, level="INFO")

# Log messages
logger.info("Application started")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)

# Change log level
set_log_level(logger, "DEBUG")
```

**Methods**:
- `get_logger(name, level)` - Create logger instance
- `set_log_level(logger, level)` - Change log level

---

## 📊 Pipeline Models

### SamplePipeline
**Location**: `src/pipelines/sample_pipeline.py`

**Class**: `SamplePipeline`

**Purpose**: Reference implementation of a complete data pipeline

**Constructor**:
```python
SamplePipeline(foundry_client, config=None)
```

**Key Methods**:
- `create_sample_data()` - Create sample DataFrame
- `run()` - Execute complete pipeline
- `main()` - Main entry point

**Pipeline Steps**:
1. Create sample data
2. Apply cleaning transform
3. Apply filtering transform
4. Display results

**Usage**:
```python
from src.pipelines.sample_pipeline import SamplePipeline
from src.foundry import FoundryClient

# Create client
client = FoundryClient(workspace_id="test", api_key="key")

# Run pipeline
pipeline = SamplePipeline(client)
result = pipeline.run()

# Clean up
client.close()
```

---

## 🧪 Testing Framework

### Transform Tests
**Location**: `tests/test_transforms.py`

**Test Functions**:
- `test_cleaning_transform_removes_duplicates()` - Verify duplicate removal
- `test_filter_transform_applies_condition()` - Verify filtering
- `test_filter_transform_without_config()` - Test missing config handling

**Running Tests**:
```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_transforms.py::test_cleaning_transform_removes_duplicates -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 🎯 Architecture Patterns

### 1. **Transform Chain Pattern**
Apply multiple transforms sequentially:

```python
from src.transforms import CleaningTransform, FilterTransform

# Create transforms
cleaning = CleaningTransform("cleaning")
filtering = FilterTransform("filtering", config={"condition": "age > 18"})

# Apply chain
df = cleaning(raw_df)
df = filtering(df)
```

### 2. **Configuration Injection Pattern**
Pass configuration to components:

```python
config = load_config()
client = FoundryClient(
    workspace_id=config.foundry_workspace,
    api_key=config.foundry_api_key,
    config=config.to_dict()
)
```

### 3. **Factory Pattern**
Create transforms dynamically:

```python
def create_transform(transform_type, name, config=None):
    if transform_type == "cleaning":
        return CleaningTransform(name)
    elif transform_type == "filter":
        return FilterTransform(name, config=config)
    elif transform_type == "aggregation":
        return AggregationTransform(name, config=config)
    else:
        raise ValueError(f"Unknown transform type: {transform_type}")

# Usage
transform = create_transform("filter", "age_filter", {"condition": "age > 18"})
```

### 4. **Dependency Injection Pattern**
Inject dependencies:

```python
class MyPipeline:
    def __init__(self, client, logger, config):
        self.client = client
        self.logger = logger
        self.config = config
    
    def run(self):
        self.logger.info(f"Running with config: {self.config}")
        # Pipeline logic
```

---

## 📦 Available Models & Types

### PySpark Models
These are available through the imported PySpark library:

**DataFrames**:
- `pyspark.sql.DataFrame` - Main data structure
- `pyspark.sql.SparkSession` - Entry point
- `pyspark.sql.Row` - Individual record

**Functions**:
- `pyspark.sql.functions` - SQL functions module
- Feature transformers: `Tokenizer`, `HashingTF`, `IDF`, `StandardScaler`
- Estimators: `LogisticRegression`, `RandomForestClassifier`
- Evaluators: `BinaryClassificationEvaluator`, `MulticlassClassificationEvaluator`

**ML Pipeline**:
- `pyspark.ml.Pipeline` - Construct ML pipelines
- `pyspark.ml.feature` - Feature engineering
- `pyspark.ml.classification` - Classification models
- `pyspark.ml.regression` - Regression models

---

## 🔗 Integration Points

### Azure Integration
**Available SDKs**:
- `azure-identity` - Authentication
- `azure-storage-blob` - Blob storage
- `azure-core` - Core functionality

**Example**:
```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
blob_client = BlobServiceClient(
    account_url=f"https://{storage_account}.blob.core.windows.net",
    credential=credential
)
```

### Delta Lake
**Configuration** (in FoundryClient):
```python
.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
```

---

## 📈 Performance Tuning

### Spark Configuration
Modify in `config/example.env`:

```env
SPARK_MASTER=local[*]           # Use all available cores
SPARK_DRIVER_MEMORY=4g          # Driver process memory
SPARK_EXECUTOR_MEMORY=2g        # Executor process memory
SPARK_SQL_SHUFFLE_PARTITIONS=200  # Shuffle partitions
```

### Batch Processing
Configure in `.env`:

```env
BATCH_SIZE=1000                 # Records per batch
MAX_RETRIES=3                   # Retry attempts
RETRY_DELAY=5                   # Seconds between retries
TIMEOUT=3600                    # Operation timeout (seconds)
```

---

## 🚀 Quick Reference

### Common Operations

**Create DataFrame**:
```python
spark = client.get_spark_session()
df = spark.createDataFrame(data, schema=["col1", "col2"])
```

**Read from File**:
```python
df = spark.read.csv("path/to/file.csv", header=True)
df = spark.read.parquet("path/to/file.parquet")
df = spark.read.json("path/to/file.json")
```

**Write to File**:
```python
df.write.csv("output/path", mode="overwrite")
df.write.parquet("output/path", mode="overwrite")
df.write.mode("overwrite").saveAsTable("my_table")
```

**Display Data**:
```python
df.show()                # Show first 20 rows
df.show(100)            # Show first 100 rows
df.display()            # In notebooks
```

**Get Info**:
```python
df.count()              # Row count
df.columns              # Column names
df.schema               # Schema
df.printSchema()        # Print schema
```

---

## 📚 Module Dependencies

### External Packages
- `pyspark>=3.5.0` - Distributed data processing
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `pydantic>=2.0.0` - Configuration validation
- `pydantic-settings>=2.0.0` - Environment settings
- `python-dotenv>=1.0.0` - Environment variables
- `pyyaml>=6.0` - YAML parsing
- `structlog>=23.1.0` - Structured logging
- `azure-identity>=1.14.0` - Azure authentication
- `azure-storage-blob>=12.18.0` - Azure Blob Storage
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Test coverage

---

## ✅ Checklist for New Components

When creating new components, ensure:

- [ ] Inherit from `BaseTransform` for transforms
- [ ] Implement `transform()` method
- [ ] Add logging for operations
- [ ] Include docstrings
- [ ] Add configuration support
- [ ] Write unit tests
- [ ] Update this catalog
- [ ] Add to module `__init__.py`
- [ ] Handle errors gracefully
- [ ] Validate inputs

---

## 📞 Support & Resources

- **Documentation**: See `README.md`, `SETUP_GUIDE.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Examples**: `src/pipelines/sample_pipeline.py`
- **Tests**: `tests/test_transforms.py`

---

**Last Updated**: May 14, 2026  
**Version**: 1.0.0  
**Project**: Microsoft Foundry Data Engineering Platform

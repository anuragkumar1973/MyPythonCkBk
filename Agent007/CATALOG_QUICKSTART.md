# Model Catalog - Quick Reference Guide

## 🚀 Quick Start

### View Catalog Summary
```bash
python catalog_viewer.py
```

### Explore Components
```bash
# Show all transforms
python catalog_viewer.py --transforms

# Show all pipelines  
python catalog_viewer.py --pipelines

# Show all models
python catalog_viewer.py --models

# Show all tags
python catalog_viewer.py --tags
```

### Find Components
```bash
# Search for components
python catalog_viewer.py --search cleaning

# Get detailed information
python catalog_viewer.py --detail CleaningTransform

# Export as JSON
python catalog_viewer.py --export json
```

---

## 📚 Available Components

### Transforms (3)

#### 1. **CleaningTransform** ✨ NEW
Removes duplicates and null values from DataFrames.

**Import**:
```python
from src.transforms import CleaningTransform
```

**Usage**:
```python
cleaning = CleaningTransform("data_cleaning")
clean_df = cleaning(raw_df)
```

**Tags**: `preprocessing`, `data-quality`, `cleaning`

---

#### 2. **FilterTransform** ⚡
Applies conditional filters to DataFrames.

**Import**:
```python
from src.transforms import FilterTransform
```

**Usage**:
```python
config = {"condition": "salary > 50000 AND age < 65"}
filter_t = FilterTransform("salary_filter", config=config)
filtered_df = filter_t(input_df)
```

**Configuration**:
```python
{
    "condition": "column_name > value"
}
```

**Tags**: `filtering`, `selection`, `data-quality`

---

#### 3. **AggregationTransform** 📊
Aggregates data using groupBy and aggregate functions.

**Import**:
```python
from src.transforms import AggregationTransform
```

**Usage**:
```python
from pyspark.sql.functions import avg, count

config = {
    "group_by": ["department", "year"],
    "aggregations": {
        "avg_salary": avg("salary"),
        "headcount": count("*")
    }
}
agg_t = AggregationTransform("dept_summary", config=config)
result = agg_t(input_df)
```

**Tags**: `aggregation`, `groupby`, `analytics`

---

### Pipelines (1)

#### **SamplePipeline** 🔄
Complete pipeline example demonstrating cleaning, filtering, and aggregation.

**Import**:
```python
from src.pipelines.sample_pipeline import SamplePipeline
```

**Usage**:
```python
# Initialize
client = FoundryClient(workspace_id="ws", api_key="key")
pipeline = SamplePipeline(client)

# Run
result = pipeline.run()

# Cleanup
client.close()
```

**Pipeline Steps**:
1. Create sample data
2. Apply cleaning
3. Filter (salary > 55000)
4. Display results

**Tags**: `pipeline`, `example`, `tutorial`

---

### Models (1)

#### **FoundryClient** 🔧
Central Foundry and Spark session management.

**Import**:
```python
from src.foundry import FoundryClient
```

**Usage**:
```python
# Create client
client = FoundryClient(
    workspace_id="your-workspace",
    api_key="your-api-key"
)

# Get Spark session
spark = client.get_spark_session()

# Use for operations
df = spark.read.csv("data.csv")

# Cleanup
client.close()
```

**Methods**:
- `get_spark_session()` - Get active Spark session
- `get_config()` - Get configuration
- `close()` - Close session

**Tags**: `framework`, `foundry`, `spark`

---

## 🏷️ Browse by Tag

### Data Quality
- CleaningTransform
- FilterTransform

### Analytics
- AggregationTransform

### Preprocessing  
- CleaningTransform

### Framework
- FoundryClient

---

## 💡 Common Patterns

### Simple Transform Chain
```python
from src.transforms import CleaningTransform, FilterTransform

# Create transforms
cleaning = CleaningTransform("cleaning")
filtering = FilterTransform("filtering", config={"condition": "age > 21"})

# Apply chain
df = cleaning(raw_df)
df = filtering(df)

# Result
df.show()
```

### Full Pipeline Example
```python
from src.foundry import FoundryClient
from src.transforms import CleaningTransform, FilterTransform, AggregationTransform
from src.utils.config import load_config

# Load configuration
config = load_config()

# Create client
client = FoundryClient(
    workspace_id=config.foundry_workspace,
    api_key=config.foundry_api_key
)

# Get Spark
spark = client.get_spark_session()

# Read data
df = spark.read.csv("employees.csv", header=True)

# Apply transforms
cleaning = CleaningTransform("clean")
df = cleaning(df)

filtering = FilterTransform("filter", config={"condition": "salary > 50000"})
df = filtering(df)

agg_config = {
    "group_by": ["department"],
    "aggregations": {
        "avg_salary": "avg",
        "count": "count"
    }
}
aggregation = AggregationTransform("agg", config=agg_config)
df = aggregation(df)

# Display results
df.show()

# Cleanup
client.close()
```

### Using with Spark Functions
```python
from pyspark.sql.functions import avg, sum, count, col

# Define aggregation
config = {
    "group_by": ["dept", "year"],
    "aggregations": {
        "total_salary": sum("salary"),
        "avg_salary": avg("salary"),
        "emp_count": count("emp_id"),
        "max_salary": max("salary")
    }
}

agg = AggregationTransform("dept_analysis", config=config)
result = agg(df)
```

---

## 📖 Component Statistics

| Metric | Value |
|--------|-------|
| Total Components | 5 |
| Active Transforms | 3 |
| Pipelines | 1 |
| Models | 1 |
| Available Tags | 14 |
| Total Tagged Items | 5 |

---

## 🔍 Searching the Catalog

### Via CLI
```bash
# Search for "filter"
python catalog_viewer.py --search filter

# Search for "aggregation"
python catalog_viewer.py --search aggregation
```

### Via Python API
```python
from src.catalog.registry import ModelCatalog

catalog = ModelCatalog()

# Search
results = catalog.search("clean")

# By tag
cleaning_components = catalog.list_by_tag("cleaning")

# By type
transforms = catalog.get_transforms()
pipelines = catalog.get_pipelines()

# Get specific component
component = catalog.get_component("CleaningTransform")
print(component.description)
print(component.examples)
```

---

## 🎓 Learning Resources

### For New Users
1. Start with `MODEL_CATALOG.md` for complete documentation
2. Review `README.md` for project overview
3. Run `demo.py` to see it in action
4. Review `src/pipelines/sample_pipeline.py` for examples

### For Developers
1. Study `src/transforms/base.py` for transform patterns
2. Review `src/foundry/__init__.py` for Foundry integration
3. Check `tests/test_transforms.py` for unit test examples
4. Use `catalog_viewer.py` as reference for Python API

### Documentation Files
- `MODEL_CATALOG.md` - Complete component documentation
- `README.md` - Project overview and setup
- `SETUP_GUIDE.md` - Detailed setup instructions
- `TROUBLESHOOTING.md` - Common issues and fixes
- `SUMMARY.md` - Project summary
- `requirements.txt` - Python dependencies

---

## 🛠️ Creating Custom Transforms

### Template
```python
from src.transforms.base import BaseTransform
from pyspark.sql import DataFrame

class MyTransform(BaseTransform):
    """Description of your transform."""
    
    def __init__(self, name: str, config: dict = None):
        super().__init__(name, config)
        # Custom initialization
    
    def transform(self, df: DataFrame) -> DataFrame:
        """Apply transformation to DataFrame."""
        # Your logic here
        return df.filter(...)

# Usage
transform = MyTransform("my_transform")
result = transform(input_df)
```

### Register in Catalog
Once created, add to `src/catalog/registry.py`:

```python
self.register(ComponentMetadata(
    name="MyTransform",
    component_type="transform",
    version="1.0.0",
    description="Your description",
    source_module="src.transforms.custom",
    class_name="MyTransform",
    examples=[...],
    tags=["category"]
))
```

---

## 📝 Examples by Use Case

### Data Cleaning
```python
cleaning = CleaningTransform("step1_clean")
df = cleaning(raw_df)
```

### Data Filtering  
```python
config = {"condition": "status = 'active' AND salary > 50000"}
filtering = FilterTransform("step2_filter", config=config)
df = filtering(df)
```

### Data Aggregation
```python
config = {
    "group_by": ["department", "region"],
    "aggregations": {"salary": "avg", "count": "count"}
}
agg = AggregationTransform("step3_aggregate", config=config)
df = agg(df)
```

### Complete ETL
```python
from src.foundry import FoundryClient
from src.transforms import CleaningTransform, FilterTransform, AggregationTransform

client = FoundryClient("workspace", "api_key")
spark = client.get_spark_session()

# Extract
df = spark.read.parquet("raw_data/")

# Transform
df = CleaningTransform("clean")(df)
df = FilterTransform("filter", config={"condition": "valid = true"})(df)
df = AggregationTransform("agg", config={...})(df)

# Load
df.write.mode("overwrite").parquet("processed_data/")

client.close()
```

---

## 🔗 Useful Commands

```bash
# View catalog summary
python catalog_viewer.py

# List all transforms
python catalog_viewer.py --transforms

# Show transform details
python catalog_viewer.py --detail CleaningTransform

# Search for components
python catalog_viewer.py --search aggregation

# List tags
python catalog_viewer.py --tags

# Export as JSON
python catalog_viewer.py --export json > catalog.json

# Run demo
python demo.py

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_transforms.py::test_cleaning_transform_removes_duplicates -v
```

---

## 📞 Need Help?

1. **View Catalog**: `python catalog_viewer.py`
2. **Get Component Details**: `python catalog_viewer.py --detail ComponentName`
3. **Search**: `python catalog_viewer.py --search query`
4. **Check Docs**: See `MODEL_CATALOG.md` and `TROUBLESHOOTING.md`
5. **Run Demo**: `python demo.py`

---

**Last Updated**: May 14, 2026  
**Version**: 1.0.0  
**Platform**: Microsoft Foundry Data Engineering

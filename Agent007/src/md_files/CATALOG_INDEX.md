# Microsoft Foundry - Model Catalog Index

## 📚 Catalog Documentation Hub

Welcome to the Microsoft Foundry Model Catalog! This is your central hub for discovering and managing all available components, transforms, and pipelines.

---

## 🚀 Quick Navigation

### For First-Time Users
1. **Start Here**: [`CATALOG_QUICKSTART.md`](CATALOG_QUICKSTART.md) - 5-minute quick start guide
2. **Explore**: Run `python catalog_viewer.py` - Interactive CLI tool
3. **Examples**: Check [`CATALOG_API_EXAMPLES.py`](CATALOG_API_EXAMPLES.py) - Code examples

### For Developers
1. **Reference**: [`MODEL_CATALOG.md`](MODEL_CATALOG.md) - Complete technical documentation
2. **API**: Use `src/catalog/registry.py` - Python API
3. **CLI**: `python catalog_viewer.py` - Command-line tool

### For Architects
1. **Implementation**: [`CATALOG_IMPLEMENTATION.md`](CATALOG_IMPLEMENTATION.md) - Architecture overview
2. **Architecture**: [`MODEL_CATALOG.md`](MODEL_CATALOG.md) - Section on patterns
3. **Integration**: See "Integration Points" below

---

## 📖 Documentation Files

| File | Purpose | Audience | Length |
|------|---------|----------|--------|
| [`CATALOG_QUICKSTART.md`](CATALOG_QUICKSTART.md) | Quick reference & examples | Everyone | ~400 lines |
| [`MODEL_CATALOG.md`](MODEL_CATALOG.md) | Complete technical reference | Developers | ~500 lines |
| [`CATALOG_API_EXAMPLES.py`](CATALOG_API_EXAMPLES.py) | Annotated code examples | Developers | ~350 lines |
| [`CATALOG_IMPLEMENTATION.md`](CATALOG_IMPLEMENTATION.md) | Implementation details | Architects | ~300 lines |
| [`catalog_viewer.py`](catalog_viewer.py) | CLI tool source code | Developers | ~350 lines |

---

## 🛠️ Tools Available

### 1. **Catalog Viewer CLI**
Interactive command-line tool for exploring the catalog.

```bash
# Show summary
python catalog_viewer.py

# View all transforms
python catalog_viewer.py --transforms

# Search for components
python catalog_viewer.py --search [query]

# Get component details
python catalog_viewer.py --detail [name]

# List all tags
python catalog_viewer.py --tags

# Export as JSON
python catalog_viewer.py --export json
```

### 2. **Python API**
Programmatic access to the catalog for automation.

```python
from src.catalog.registry import ModelCatalog

catalog = ModelCatalog()

# Search
results = catalog.search("cleaning")

# By tag
quality = catalog.list_by_tag("data-quality")

# Get details
component = catalog.get_component("CleaningTransform")
```

---

## 📊 Catalog Overview

### Components (5 Total)

**Transforms (3)**:
- 🧹 **CleaningTransform** - Remove duplicates and null values
- 🔍 **FilterTransform** - Apply conditional filters
- 📊 **AggregationTransform** - Group and aggregate data

**Pipelines (1)**:
- 🔄 **SamplePipeline** - Reference pipeline example

**Models (1)**:
- 🔧 **FoundryClient** - Central Foundry integration

### Tags (14 Total)
`aggregation` `analytics` `cleaning` `data-quality` `example` `filtering` `foundry` `framework` `groupby` `pipeline` `preprocessing` `selection` `spark` `tutorial`

---

## 💡 Common Tasks

### Find a Transform
```bash
python catalog_viewer.py --transforms
```

### Search by Tag
```bash
python catalog_viewer.py --search data-quality
```

### Get Component Details
```bash
python catalog_viewer.py --detail CleaningTransform
```

### Use in Code
```python
from src.transforms import CleaningTransform

cleaning = CleaningTransform("step1")
result = cleaning(input_df)
```

### Browse All Tags
```bash
python catalog_viewer.py --tags
```

### Export Catalog
```bash
python catalog_viewer.py --export json > catalog.json
```

---

## 🎯 Use Cases

### 1. **Data Cleaning**
- Component: `CleaningTransform`
- Tags: `preprocessing`, `data-quality`
- Documentation: See CATALOG_QUICKSTART.md

### 2. **Data Filtering**
- Component: `FilterTransform`
- Tags: `filtering`, `selection`
- Documentation: See CATALOG_QUICKSTART.md

### 3. **Data Aggregation**
- Component: `AggregationTransform`
- Tags: `aggregation`, `analytics`
- Documentation: See MODEL_CATALOG.md

### 4. **Complete ETL Pipeline**
- Use: `SamplePipeline`
- Or combine transforms manually
- Examples: See CATALOG_QUICKSTART.md

---

## 🔍 Component Directory

### CleaningTransform
**Type**: Transform  
**Purpose**: Remove duplicates and null values  
**Source**: `src/transforms/base.py`  
**Tags**: `preprocessing`, `data-quality`, `cleaning`  
**Status**: Active  

→ View with: `python catalog_viewer.py --detail CleaningTransform`

---

### FilterTransform
**Type**: Transform  
**Purpose**: Apply conditional filters  
**Source**: `src/transforms/base.py`  
**Tags**: `filtering`, `selection`, `data-quality`  
**Status**: Active  

→ View with: `python catalog_viewer.py --detail FilterTransform`

---

### AggregationTransform
**Type**: Transform  
**Purpose**: Group and aggregate data  
**Source**: `src/transforms/base.py`  
**Tags**: `aggregation`, `groupby`, `analytics`  
**Status**: Active  

→ View with: `python catalog_viewer.py --detail AggregationTransform`

---

### SamplePipeline
**Type**: Pipeline  
**Purpose**: Reference pipeline example  
**Source**: `src/pipelines/sample_pipeline.py`  
**Tags**: `pipeline`, `example`, `tutorial`  
**Status**: Active  

→ View with: `python catalog_viewer.py --detail SamplePipeline`

---

### FoundryClient
**Type**: Model  
**Purpose**: Central Foundry integration  
**Source**: `src/foundry/__init__.py`  
**Tags**: `framework`, `foundry`, `spark`  
**Status**: Active  

→ View with: `python catalog_viewer.py --detail FoundryClient`

---

## 📚 Learning Paths

### Path 1: Quick Start (15 minutes)
1. Read: [`CATALOG_QUICKSTART.md`](CATALOG_QUICKSTART.md) - 10 min
2. Run: `python catalog_viewer.py` - 2 min
3. Try: `python catalog_viewer.py --transforms` - 3 min

### Path 2: Developer Onboarding (1 hour)
1. Read: [`CATALOG_QUICKSTART.md`](CATALOG_QUICKSTART.md) - 15 min
2. Study: [`CATALOG_API_EXAMPLES.py`](CATALOG_API_EXAMPLES.py) - 20 min
3. Explore: `python catalog_viewer.py --detail [component]` - 15 min
4. Practice: Write code using API - 10 min

### Path 3: Deep Dive (2 hours)
1. Read: [`MODEL_CATALOG.md`](MODEL_CATALOG.md) - 45 min
2. Study: [`src/catalog/registry.py`](src/catalog/registry.py) - 45 min
3. Review: Source files - 20 min
4. Implement: Custom transforms - 10 min

---

## 🔗 Related Documentation

| Document | Topic | Link |
|----------|-------|------|
| README | Project overview | `README.md` |
| Setup Guide | Installation & setup | `SETUP_GUIDE.md` |
| Troubleshooting | Common issues | `TROUBLESHOOTING.md` |
| Summary | Project summary | `SUMMARY.md` |
| Requirements | Dependencies | `requirements.txt` |

---

## 🏗️ Architecture Overview

```
Model Catalog
├── CLI Interface (catalog_viewer.py)
├── Python API (src/catalog/registry.py)
│   ├── ComponentMetadata - Metadata container
│   ├── ModelCatalog - Main catalog
│   └── TransformRegistry - Transform-specific registry
└── Documentation
    ├── Quick Start Guide
    ├── Complete Reference
    ├── API Examples
    └── Implementation Details
```

---

## 🔄 Workflow Examples

### Discover → Understand → Use

```
1. Discover
   python catalog_viewer.py
   python catalog_viewer.py --search [topic]

2. Understand
   python catalog_viewer.py --detail [name]
   Read CATALOG_QUICKSTART.md

3. Use
   from src.transforms import CleaningTransform
   transform = CleaningTransform("name")
   result = transform(df)
```

### Search → Filter → Apply

```
1. Search
   catalog.search("quality")

2. Filter
   components = catalog.list_by_tag("preprocessing")

3. Apply
   for component in components:
       transform = create_from_metadata(component)
       df = transform(df)
```

---

## 🚀 Getting Started

### Option 1: CLI Tool (Recommended for exploration)
```bash
python catalog_viewer.py
```

### Option 2: Python API (For automation)
```python
from src.catalog.registry import ModelCatalog
catalog = ModelCatalog()
results = catalog.search("filter")
```

### Option 3: Documentation (For learning)
Start with [`CATALOG_QUICKSTART.md`](CATALOG_QUICKSTART.md)

---

## 📈 Statistics

| Metric | Value |
|--------|-------|
| Components Registered | 5 |
| Transforms | 3 |
| Pipelines | 1 |
| Models | 1 |
| Available Tags | 14 |
| Documentation Pages | 5 |
| Code Examples | 50+ |

---

## ✅ Checklist: Getting Started

- [ ] Read CATALOG_QUICKSTART.md
- [ ] Run `python catalog_viewer.py`
- [ ] Explore with `--transforms` flag
- [ ] View details with `--detail` flag
- [ ] Try search with `--search` flag
- [ ] Review CATALOG_API_EXAMPLES.py
- [ ] Use Python API in your code
- [ ] Reference MODEL_CATALOG.md for details

---

## 🆘 Need Help?

### Quick Questions
→ Check [`CATALOG_QUICKSTART.md`](CATALOG_QUICKSTART.md)

### Detailed Reference
→ Read [`MODEL_CATALOG.md`](MODEL_CATALOG.md)

### Code Examples
→ Study [`CATALOG_API_EXAMPLES.py`](CATALOG_API_EXAMPLES.py)

### Technical Details
→ Review [`CATALOG_IMPLEMENTATION.md`](CATALOG_IMPLEMENTATION.md)

### Interactive Exploration
→ Run `python catalog_viewer.py`

---

## 🎓 Key Concepts

### ComponentMetadata
Structured information about a component including name, type, description, parameters, examples, and tags.

### ModelCatalog
Central registry storing all components and providing search, filter, and retrieval capabilities.

### TransformRegistry
Specialized registry focusing on data transforms with category-specific methods.

### Tags
Flexible labels for categorizing and discovering components (e.g., "preprocessing", "analytics").

### Status
Component status: `active`, `deprecated`, or `experimental`.

---

## 🔐 Best Practices

1. **Explore First**: Use `catalog_viewer.py` to understand available components
2. **Read Examples**: Check examples in CATALOG_QUICKSTART.md
3. **Check Parameters**: Review component details before using
4. **Use Tags**: Filter by tags for category-specific components
5. **Document Custom**: Add metadata when creating custom transforms
6. **Version Components**: Use semantic versioning (e.g., 1.0.0)

---

## 📝 Creating Custom Components

1. Create the component class (inherit from BaseTransform)
2. Create ComponentMetadata with full documentation
3. Register in catalog: `catalog.register(metadata)`
4. Test with `catalog_viewer.py --detail [name]`
5. Document in README or CATALOG_QUICKSTART.md

---

## 🌟 What's Next?

After exploring the catalog:

1. **Try Examples**: Run code from CATALOG_API_EXAMPLES.py
2. **Build Pipeline**: Combine transforms into a pipeline
3. **Create Custom**: Build your own transforms
4. **Extend Catalog**: Register new components
5. **Share**: Export catalog and share with team

---

## 📞 Support Resources

| Topic | Resource |
|-------|----------|
| Getting Started | CATALOG_QUICKSTART.md |
| Technical Details | MODEL_CATALOG.md |
| Code Examples | CATALOG_API_EXAMPLES.py |
| Implementation | CATALOG_IMPLEMENTATION.md |
| CLI Tool | catalog_viewer.py |
| API Reference | src/catalog/registry.py |

---

**Last Updated**: May 14, 2026  
**Version**: 1.0.0  
**Status**: Production Ready

---

## 📋 Document Map

```
📚 Documentation
├── 🚀 CATALOG_QUICKSTART.md (START HERE)
├── 📖 MODEL_CATALOG.md (Reference)
├── 💻 CATALOG_API_EXAMPLES.py (Code)
├── 🏗️ CATALOG_IMPLEMENTATION.md (Architecture)
├── 🔧 catalog_viewer.py (CLI Tool)
└── 📑 INDEX.md (This file)
```

Start with the Quick Start Guide, then explore based on your needs!

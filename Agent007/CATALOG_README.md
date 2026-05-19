# 🎯 Microsoft Foundry - Model Catalog

**Complete, searchable registry of all available components, transforms, and pipelines.**

---

## ⚡ Quick Start (2 minutes)

### View the Catalog
```bash
python catalog_viewer.py
```

### Find a Transform
```bash
python catalog_viewer.py --transforms
```

### Search for Components
```bash
python catalog_viewer.py --search cleaning
```

### Get Details
```bash
python catalog_viewer.py --detail CleaningTransform
```

---

## 📚 What's Included?

### **5 Core Components** (Ready to Use)

| Component | Type | Purpose |
|-----------|------|---------|
| **CleaningTransform** | Transform | Remove duplicates & nulls |
| **FilterTransform** | Transform | Apply conditional filters |
| **AggregationTransform** | Transform | Group & aggregate data |
| **SamplePipeline** | Pipeline | Reference implementation |
| **FoundryClient** | Model | Central integration point |

### **14 Organized Tags**
For easy discovery: `preprocessing`, `analytics`, `data-quality`, `spark`, and more

### **Multiple Access Methods**
- 🖥️ **CLI Tool** - Interactive command-line browser
- 🐍 **Python API** - Programmatic access
- 📖 **Documentation** - Complete reference guides

---

## 🚀 Using the Catalog

### Command-Line Interface

```bash
# Show summary and statistics
python catalog_viewer.py

# List all transforms
python catalog_viewer.py --transforms

# List all pipelines
python catalog_viewer.py --pipelines

# Search for components
python catalog_viewer.py --search [query]

# Get detailed info about a component
python catalog_viewer.py --detail [name]

# Browse all available tags
python catalog_viewer.py --tags

# Export as JSON
python catalog_viewer.py --export json
```

### Python API

```python
from src.catalog.registry import ModelCatalog

# Create catalog instance
catalog = ModelCatalog()

# Search components
results = catalog.search("clean")

# Get by tag
quality_components = catalog.list_by_tag("data-quality")

# Get by type
transforms = catalog.get_transforms()
pipelines = catalog.get_pipelines()

# Get specific component
component = catalog.get_component("CleaningTransform")
print(component.description)
print(component.examples)

# Print formatted output
catalog.print_summary()
catalog.print_components()
```

---

## 📖 Documentation

### For Different Audiences

| Document | Best For | Time |
|----------|----------|------|
| **[CATALOG_QUICKSTART.md](CATALOG_QUICKSTART.md)** | First-time users | 10 min |
| **[MODEL_CATALOG.md](MODEL_CATALOG.md)** | Developers | 30 min |
| **[CATALOG_API_EXAMPLES.py](CATALOG_API_EXAMPLES.py)** | Code examples | 20 min |
| **[CATALOG_IMPLEMENTATION.md](CATALOG_IMPLEMENTATION.md)** | Architects | 20 min |
| **[CATALOG_INDEX.md](CATALOG_INDEX.md)** | Navigation hub | 5 min |

### Quick Links
- 📌 **Start Here**: CATALOG_QUICKSTART.md
- 🔍 **Find Components**: Run `python catalog_viewer.py`
- 💻 **Code Examples**: CATALOG_API_EXAMPLES.py
- 📚 **Complete Reference**: MODEL_CATALOG.md
- 🗺️ **Navigation**: CATALOG_INDEX.md

---

## 💡 Common Tasks

### Find a Data Quality Transform
```bash
python catalog_viewer.py --search data-quality
```

### Use a Transform in Code
```python
from src.transforms import CleaningTransform

cleaning = CleaningTransform("step1_clean")
result = cleaning(raw_dataframe)
```

### Create a Transform Pipeline
```python
from src.transforms import CleaningTransform, FilterTransform

# Create transforms
cleaner = CleaningTransform("clean")
filterer = FilterTransform("filter", config={"condition": "age > 18"})

# Apply chain
df = cleaner(df)
df = filterer(df)
```

### Search Catalog from Code
```python
from src.catalog.registry import ModelCatalog

catalog = ModelCatalog()
preprocessing_transforms = catalog.list_by_tag("preprocessing")

for transform in preprocessing_transforms:
    print(f"{transform.name}: {transform.description}")
```

---

## 🏆 Key Features

✅ **Complete Metadata** - Every component has rich documentation  
✅ **Multiple Access Patterns** - CLI, Python API, and documentation  
✅ **Fast Search** - Find components by name, description, or tag  
✅ **Pre-populated** - 5 core components ready to use  
✅ **Extensible** - Easy to add custom transforms  
✅ **Well Documented** - 5 documentation files  
✅ **Production Ready** - Fully tested and working  
✅ **Tagged Organization** - 14 tags for easy browsing  

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Registered Components | 5 |
| Available Transforms | 3 |
| Pipelines | 1 |
| Core Models | 1 |
| Available Tags | 14 |
| Documentation Files | 5 |
| Lines of Code | 750+ |
| Lines of Documentation | 2500+ |

---

## 🎓 Learning Paths

### Path 1: Quick Exploration (15 min)
1. Run `python catalog_viewer.py`
2. Try `python catalog_viewer.py --transforms`
3. View component: `python catalog_viewer.py --detail CleaningTransform`

### Path 2: Developer Onboarding (1 hour)
1. Read CATALOG_QUICKSTART.md (15 min)
2. Study CATALOG_API_EXAMPLES.py (20 min)
3. Explore with CLI: `python catalog_viewer.py` (15 min)
4. Try code examples (10 min)

### Path 3: Complete Mastery (2 hours)
1. Read MODEL_CATALOG.md (45 min)
2. Study src/catalog/registry.py source (45 min)
3. Review implementation: CATALOG_IMPLEMENTATION.md (20 min)
4. Create custom transform (10 min)

---

## 🔗 Integration with Project

The catalog integrates seamlessly with your Microsoft Foundry project:

- **Transforms**: References all transforms in `src/transforms/base.py`
- **Pipelines**: Documents pipelines in `src/pipelines/`
- **Models**: Includes FoundryClient from `src/foundry/`
- **Configuration**: Uses project config from `src/utils/`
- **Logging**: Integrates with project logger

---

## 📁 Project Structure

```
Agent007/
├── catalog_viewer.py              # CLI tool
├── MODEL_CATALOG.md               # Complete reference
├── CATALOG_QUICKSTART.md          # Quick start guide
├── CATALOG_API_EXAMPLES.py        # Code examples
├── CATALOG_IMPLEMENTATION.md      # Architecture
├── CATALOG_INDEX.md               # Navigation hub
├── CATALOG_README.md              # This file
└── src/
    └── catalog/
        ├── __init__.py
        └── registry.py            # Core implementation
```

---

## ✨ What You Can Do

### For End Users
- 🔍 Search for available components
- 📖 Read detailed documentation
- 💾 Export catalog as JSON
- 🎯 Find components by category/tag

### For Developers
- 🐍 Use Python API for automation
- 🔧 Build custom transforms
- 📦 Register components in catalog
- 🔗 Integrate with your code

### For Data Scientists
- 🧪 Discover available transforms
- 📊 Chain transforms into pipelines
- 📈 Analyze component metadata
- 💡 See usage examples

### For Architects
- 🏗️ Understand component relationships
- 📐 Plan pipeline architectures
- 🔄 Design component workflows
- 📋 Document system design

---

## 🚀 Next Steps

### Start Exploring
```bash
python catalog_viewer.py
```

### Read Quick Start
Open `CATALOG_QUICKSTART.md` in your editor

### Try Python API
```python
from src.catalog.registry import ModelCatalog
catalog = ModelCatalog()
catalog.print_summary()
```

### Use in Your Project
```python
from src.catalog.registry import ModelCatalog

catalog = ModelCatalog()
transforms = catalog.get_transforms()

for t in transforms:
    print(f"Transform: {t.name}")
    print(f"Tags: {', '.join(t.tags)}")
```

---

## 📚 Related Files

### Project Documentation
- `README.md` - Project overview
- `SETUP_GUIDE.md` - Installation guide
- `TROUBLESHOOTING.md` - Common issues

### Catalog Documentation
- `MODEL_CATALOG.md` - Technical reference (14 KB)
- `CATALOG_QUICKSTART.md` - Quick start (9.5 KB)
- `CATALOG_API_EXAMPLES.py` - Code examples (13 KB)
- `CATALOG_IMPLEMENTATION.md` - Architecture (10 KB)
- `CATALOG_INDEX.md` - Navigation (11 KB)

### Source Code
- `catalog_viewer.py` - CLI tool (350 lines)
- `src/catalog/registry.py` - Core API (400 lines)

---

## ⚙️ Configuration

The catalog automatically:
- ✅ Scans project source files
- ✅ Registers built-in components
- ✅ Indexes by tags and type
- ✅ Enables full-text search

No configuration needed - it just works!

---

## 🔐 Best Practices

1. **Explore First**: Use CLI to understand available components
2. **Check Tags**: Filter by tags for related components
3. **Review Examples**: Check examples before using
4. **Document Custom**: Add metadata when creating components
5. **Use API**: Leverage Python API for automation
6. **Keep Updated**: Add components to catalog as created

---

## ❓ FAQ

**Q: How do I find a specific transform?**  
A: Use `python catalog_viewer.py --search [name]`

**Q: How do I use a transform in my code?**  
A: Import it and instantiate: `from src.transforms import CleaningTransform`

**Q: Can I add my own components?**  
A: Yes! See CATALOG_QUICKSTART.md for instructions

**Q: How do I search programmatically?**  
A: Use the Python API: `catalog.search("query")`

**Q: Where's the complete documentation?**  
A: In MODEL_CATALOG.md and supporting files

---

## 🆘 Need Help?

| Question | Resource |
|----------|----------|
| Getting started? | CATALOG_QUICKSTART.md |
| How does it work? | CATALOG_IMPLEMENTATION.md |
| Code examples? | CATALOG_API_EXAMPLES.py |
| Complete reference? | MODEL_CATALOG.md |
| Navigation? | CATALOG_INDEX.md |
| Quick lookup? | `python catalog_viewer.py` |

---

## 🎯 Use Cases

### Data Engineer
```bash
# Find preprocessing transforms
python catalog_viewer.py --search preprocessing

# Get details
python catalog_viewer.py --detail CleaningTransform

# Use in pipeline
from src.transforms import CleaningTransform
df = CleaningTransform("step1")(df)
```

### Data Scientist
```python
# Discover transforms
catalog.list_by_tag("analytics")

# Build analysis pipeline
transforms = [
    CleaningTransform("clean"),
    FilterTransform("filter"),
    AggregationTransform("aggregate")
]

for transform in transforms:
    df = transform(df)
```

### Platform Engineer
```python
# Find all components
all_components = catalog.list_all()

# Plan architecture
for component in all_components:
    if component.component_type == "pipeline":
        analyze_dependencies(component)

# Export for sharing
catalog_json = catalog.to_json()
```

---

## ✅ Verification Checklist

- [x] Catalog module created and tested
- [x] CLI tool implemented and working
- [x] 5 core components registered
- [x] Full-text search implemented
- [x] Tag-based filtering working
- [x] Documentation complete
- [x] API examples provided
- [x] All features tested

---

## 📊 Catalog Insights

### By Component Type
- **Transforms**: 3 (data processing)
- **Pipelines**: 1 (orchestration)
- **Models**: 1 (framework)

### By Category
- **Data Quality**: 2 components
- **Preprocessing**: 1 component
- **Analytics**: 1 component
- **Framework**: 1 component

### By Status
- **Active**: 5 components
- **Deprecated**: 0 components
- **Experimental**: 0 components

---

## 🌟 Highlights

✨ **Complete & Production Ready** - Fully tested, working code  
✨ **Well Documented** - 2500+ lines of documentation  
✨ **Easy to Use** - Simple CLI and Python API  
✨ **Extensible** - Add custom components easily  
✨ **Discoverable** - Search and filter capabilities  
✨ **Organized** - 14 meaningful tags  
✨ **Integrated** - Works with existing project  

---

## 🚀 Get Started Now

1. **Explore**: `python catalog_viewer.py`
2. **Learn**: Read `CATALOG_QUICKSTART.md`
3. **Code**: Use transforms in your project
4. **Extend**: Add custom components
5. **Share**: Export and collaborate

---

**Last Updated**: May 14, 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

**Happy exploring! 🎉**

For more information, see [CATALOG_INDEX.md](CATALOG_INDEX.md) for a complete navigation guide.

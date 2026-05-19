"""
Model Catalog API Documentation

This module demonstrates how to use the Model Catalog API programmatically.
The catalog provides a registry of available transforms, pipelines, and models.
"""

# ==============================================================================
# BASIC USAGE
# ==============================================================================

"""
Import the catalog:
"""
from src.catalog.registry import ModelCatalog, TransformRegistry

# Create catalog instance
catalog = ModelCatalog()

# ==============================================================================
# QUERYING THE CATALOG
# ==============================================================================

# Get all components
all_components = catalog.list_all()
print(f"Total components: {len(all_components)}")

# Get by type
transforms = catalog.get_transforms()        # Get all transforms
pipelines = catalog.get_pipelines()          # Get all pipelines
models = catalog.get_models()                # Get all models

# Get specific component
component = catalog.get_component("CleaningTransform")
print(f"Component: {component.name}")
print(f"Description: {component.description}")

# Get multiple components
components = catalog.get_components([
    "CleaningTransform",
    "FilterTransform",
    "SamplePipeline"
])

# ==============================================================================
# SEARCHING
# ==============================================================================

# Search by name or description
results = catalog.search("cleaning")
results = catalog.search("filter")
results = catalog.search("aggregat")

# Get by tag
preprocessing = catalog.list_by_tag("preprocessing")
analytics = catalog.list_by_tag("analytics")
data_quality = catalog.list_by_tag("data-quality")

# Get by status
active = catalog.list_by_status("active")
deprecated = catalog.list_by_status("deprecated")

# Get all tags
tags = catalog.get_tags()
print(f"Available tags: {tags}")

# ==============================================================================
# COMPONENT METADATA
# ==============================================================================

# Access component properties
component = catalog.get_component("CleaningTransform")

print(f"Name: {component.name}")
print(f"Type: {component.component_type}")
print(f"Version: {component.version}")
print(f"Status: {component.status}")
print(f"Description: {component.description}")
print(f"Author: {component.author}")
print(f"Created: {component.created_date}")

# Access source information
print(f"Module: {component.source_module}")
print(f"Class: {component.class_name}")

# Access parameters
for param_name, param_info in component.parameters.items():
    print(f"Parameter: {param_name}")
    print(f"  Type: {param_info.get('type')}")
    print(f"  Required: {param_info.get('required')}")
    print(f"  Description: {param_info.get('description')}")

# Access usage examples
print("Examples:")
for example in component.examples:
    print(f"  {example}")

# Access tags
print(f"Tags: {component.tags}")

# ==============================================================================
# EXPORTING CATALOG
# ==============================================================================

# Export to dictionary
catalog_dict = catalog.to_dict()
print(f"Statistics: {catalog_dict['stats']}")

# Export to JSON
catalog_json = catalog.to_json()
print(catalog_json)

# ==============================================================================
# TRANSFORM REGISTRY
# ==============================================================================

# Use specialized transform registry
transform_registry = TransformRegistry(catalog)

# Get all transforms
all_transforms = transform_registry.get_all_transforms()

# Get specific transform
cleaning = transform_registry.get_transform("CleaningTransform")

# Get by category
preprocessing_transforms = transform_registry.list_preprocessing_transforms()
filtering_transforms = transform_registry.list_filtering_transforms()
aggregation_transforms = transform_registry.list_aggregation_transforms()

# ==============================================================================
# PRINTING CATALOG
# ==============================================================================

# Print summary
catalog.print_summary()

# Print all components
catalog.print_components()

# Print specific components
transforms = catalog.get_transforms()
catalog.print_components(transforms)

# ==============================================================================
# REGISTERING CUSTOM COMPONENTS
# ==============================================================================

from src.catalog.registry import ComponentMetadata

# Create metadata for custom component
custom_metadata = ComponentMetadata(
    name="CustomTransform",
    component_type="transform",
    version="1.0.0",
    description="My custom data transformation",
    author="Your Name",
    source_module="src.transforms.custom",
    class_name="CustomTransform",
    parameters={
        "name": {
            "type": "str",
            "required": True,
            "description": "Transform name"
        },
        "threshold": {
            "type": "float",
            "required": False,
            "description": "Threshold value"
        }
    },
    examples=[
        "transform = CustomTransform('my_transform', threshold=0.5)",
        "result = transform(input_df)"
    ],
    tags=["custom", "filtering"],
    status="active"
)

# Register in catalog
try:
    catalog.register(custom_metadata)
    print("Custom component registered successfully")
except ValueError as e:
    print(f"Registration failed: {e}")

# ==============================================================================
# PRACTICAL EXAMPLES
# ==============================================================================

# Example 1: Find all data quality transforms
print("\n=== Example 1: Find Data Quality Transforms ===")
quality_transforms = catalog.list_by_tag("data-quality")
for transform in quality_transforms:
    print(f"- {transform.name}: {transform.description}")

# Example 2: Get transform details for documentation
print("\n=== Example 2: Generate Transform Documentation ===")
for transform in catalog.get_transforms():
    print(f"\n## {transform.name}")
    print(f"- Description: {transform.description}")
    print(f"- Module: {transform.source_module}")
    print(f"- Tags: {', '.join(transform.tags)}")
    print(f"- Parameters: {', '.join(transform.parameters.keys())}")

# Example 3: Build transform pipeline programmatically
print("\n=== Example 3: Build Transform Pipeline ===")
pipeline_steps = [
    "CleaningTransform",
    "FilterTransform",
    "AggregationTransform"
]

for step_name in pipeline_steps:
    component = catalog.get_component(step_name)
    print(f"Step: {component.name}")
    print(f"  Type: {component.component_type}")
    print(f"  Description: {component.description}")

# Example 4: Search and display matching components
print("\n=== Example 4: Search Components ===")
search_query = "filter"
results = catalog.search(search_query)
print(f"Search results for '{search_query}':")
for result in results:
    print(f"- {result.name} ({result.component_type})")
    print(f"  {result.description}")

# Example 5: Generate component inventory
print("\n=== Example 5: Component Inventory ===")
inventory = catalog.to_dict()
print(f"Total: {inventory['stats']['total_components']}")
for ctype, count in inventory['stats']['by_type'].items():
    print(f"- {ctype}: {count}")

# ==============================================================================
# WORKING WITH COMPONENT METADATA
# ==============================================================================

# Convert to different formats
component = catalog.get_component("FilterTransform")

# To dictionary
component_dict = component.to_dict()

# To JSON
component_json = component.to_json()

# Print formatted
print(f"\nComponent: {component.name}")
print(f"JSON:\n{component_json}")

# ==============================================================================
# FILTERING AND NAVIGATION
# ==============================================================================

# Find components by multiple criteria
print("\n=== Multi-criteria Filtering ===")

# Find active preprocessing transforms
all_transforms = catalog.get_transforms()
preprocessing = [c for c in all_transforms 
                if "preprocessing" in c.tags 
                and c.status == "active"]

print(f"Active preprocessing transforms: {len(preprocessing)}")
for p in preprocessing:
    print(f"- {p.name}")

# Find components by author
foundry_components = [c for c in catalog.list_all() 
                     if c.author == "Microsoft Foundry"]
print(f"\nComponents by Microsoft Foundry: {len(foundry_components)}")

# ==============================================================================
# CATALOG STATISTICS
# ==============================================================================

print("\n=== Catalog Statistics ===")
stats = catalog.to_dict()["stats"]
print(f"Total components: {stats['total_components']}")
print(f"Types: {stats['by_type']}")
print(f"Status: {stats['by_status']}")
print(f"Tags: {stats['total_tags']}")

# ==============================================================================
# COMPONENT GRAPH/DEPENDENCIES
# ==============================================================================

"""
Example: Understanding component relationships

SamplePipeline uses:
- CleaningTransform
- FilterTransform

These transforms can be chained together in any pipeline.
"""

# Find components used by a pipeline
print("\n=== Pipeline Components ===")
sample_pipeline = catalog.get_component("SamplePipeline")
print(f"Pipeline: {sample_pipeline.name}")
print(f"Description: {sample_pipeline.description}")
print(f"Uses transforms: CleaningTransform, FilterTransform, AggregationTransform")

# ==============================================================================
# LOGGING AND DEBUGGING
# ==============================================================================

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Log component access
component = catalog.get_component("CleaningTransform")
logger.info(f"Accessed component: {component.name}")

# Log searches
results = catalog.search("agg")
logger.info(f"Search for 'agg' returned {len(results)} results")

# ==============================================================================
# BEST PRACTICES
# ==============================================================================

"""
1. Cache catalog instance:
   catalog = ModelCatalog()  # Create once, reuse
   
2. Use specialized registries when appropriate:
   transform_registry = TransformRegistry(catalog)
   
3. Search before iterating:
   results = catalog.search("query")  # Better than looping all
   
4. Check status before using:
   active = catalog.list_by_status("active")
   
5. Document custom components:
   Always include description, examples, and tags
   
6. Version your components:
   Use semantic versioning (1.0.0)
   
7. Use tags effectively:
   Makes searching and filtering easier
"""

# ==============================================================================
# ERROR HANDLING
# ==============================================================================

# Check if component exists
component_name = "NonExistent"
component = catalog.get_component(component_name)
if component is None:
    print(f"Component '{component_name}' not found")

# Handle registration errors
try:
    # Try to register duplicate
    catalog.register(custom_metadata)
except ValueError as e:
    print(f"Error: {e}")

# Handle empty results
results = catalog.search("nonexistent")
if not results:
    print("No components found matching query")

# ==============================================================================
# COMPLETE WORKFLOW EXAMPLE
# ==============================================================================

print("\n=== Complete Workflow Example ===")

# 1. Initialize catalog
catalog = ModelCatalog()

# 2. Search for data quality components
quality_components = catalog.list_by_tag("data-quality")
print(f"Found {len(quality_components)} data quality components")

# 3. Get details for each
for component in quality_components:
    print(f"\n{component.name}")
    print(f"  Description: {component.description}")
    print(f"  Parameters: {list(component.parameters.keys())}")
    print(f"  Examples: {len(component.examples)}")

# 4. Build transform list
transform_list = [c.name for c in catalog.get_transforms()]
print(f"\nAvailable transforms for pipeline: {transform_list}")

# 5. Export for use
catalog_data = catalog.to_dict()
print(f"\nExported {catalog_data['stats']['total_components']} components")

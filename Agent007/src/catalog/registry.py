"""
Model and Transform Registry for the Foundry Platform.

This module provides programmatic access to available models,
transforms, and pipelines in the Microsoft Foundry project.
"""

import json
from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class ComponentMetadata:
    """Metadata for a component (transform, model, or pipeline)."""
    
    name: str
    component_type: str  # "transform", "model", "pipeline"
    version: str = "1.0.0"
    description: str = ""
    author: str = "Microsoft Foundry"
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_date: str = field(default_factory=lambda: datetime.now().isoformat())
    source_module: str = ""
    class_name: str = ""
    required_columns: List[str] = field(default_factory=list)
    output_columns: List[str] = field(default_factory=list)
    parameters: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    examples: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    status: str = "active"  # active, deprecated, experimental
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert metadata to JSON."""
        return json.dumps(self.to_dict(), indent=2)


class ModelCatalog:
    """
    Centralized catalog of all available models, transforms, and pipelines.
    
    Example:
        >>> catalog = ModelCatalog()
        >>> transforms = catalog.get_transforms()
        >>> cleaning = catalog.get_component("CleaningTransform")
        >>> catalog.list_by_tag("preprocessing")
    """
    
    def __init__(self):
        """Initialize the model catalog with built-in components."""
        self._components: Dict[str, ComponentMetadata] = {}
        self._indices: Dict[str, Dict[str, List[str]]] = {
            "type": {},
            "tag": {},
            "status": {}
        }
        self._register_builtin_components()
    
    def _register_builtin_components(self):
        """Register built-in transforms and pipelines."""
        
        # CleaningTransform
        self.register(ComponentMetadata(
            name="CleaningTransform",
            component_type="transform",
            version="1.0.0",
            description="Remove duplicates and null values from DataFrame",
            author="Microsoft Foundry",
            source_module="src.transforms.base",
            class_name="CleaningTransform",
            output_columns=["*"],
            parameters={
                "name": {
                    "type": "str",
                    "required": True,
                    "description": "Name of this transform instance"
                }
            },
            examples=[
                "cleaning = CleaningTransform('data_cleaning')",
                "clean_df = cleaning(raw_df)"
            ],
            tags=["preprocessing", "data-quality", "cleaning"],
            status="active"
        ))
        
        # FilterTransform
        self.register(ComponentMetadata(
            name="FilterTransform",
            component_type="transform",
            version="1.0.0",
            description="Apply conditional filters to DataFrame",
            author="Microsoft Foundry",
            source_module="src.transforms.base",
            class_name="FilterTransform",
            output_columns=["*"],
            parameters={
                "name": {
                    "type": "str",
                    "required": True,
                    "description": "Name of this transform instance"
                },
                "config": {
                    "type": "dict",
                    "required": False,
                    "description": "Configuration dict with 'condition' key",
                    "example": '{"condition": "salary > 50000"}'
                }
            },
            examples=[
                "config = {'condition': 'status == \"active\"'}",
                "filter_t = FilterTransform('status_filter', config=config)",
                "filtered = filter_t(df)"
            ],
            tags=["filtering", "selection", "data-quality"],
            status="active"
        ))
        
        # AggregationTransform
        self.register(ComponentMetadata(
            name="AggregationTransform",
            component_type="transform",
            version="1.0.0",
            description="Aggregate data using groupBy and aggregate functions",
            author="Microsoft Foundry",
            source_module="src.transforms.base",
            class_name="AggregationTransform",
            parameters={
                "name": {
                    "type": "str",
                    "required": True,
                    "description": "Name of this transform instance"
                },
                "config": {
                    "type": "dict",
                    "required": False,
                    "description": "Configuration with group_by and aggregations",
                    "example": '{"group_by": ["dept"], "aggregations": {"salary": "avg"}}'
                }
            },
            examples=[
                "from pyspark.sql.functions import avg",
                "config = {'group_by': ['dept'], 'aggregations': {'salary': avg('salary')}}",
                "agg_t = AggregationTransform('dept_summary', config=config)",
                "result = agg_t(df)"
            ],
            tags=["aggregation", "groupby", "analytics"],
            status="active"
        ))
        
        # SamplePipeline
        self.register(ComponentMetadata(
            name="SamplePipeline",
            component_type="pipeline",
            version="1.0.0",
            description="Reference pipeline demonstrating cleaning, filtering, and aggregation",
            author="Microsoft Foundry",
            source_module="src.pipelines.sample_pipeline",
            class_name="SamplePipeline",
            parameters={
                "foundry_client": {
                    "type": "FoundryClient",
                    "required": True,
                    "description": "Foundry client instance"
                },
                "config": {
                    "type": "dict",
                    "required": False,
                    "description": "Optional configuration override"
                }
            },
            examples=[
                "from src.pipelines.sample_pipeline import SamplePipeline",
                "pipeline = SamplePipeline(foundry_client)",
                "result_df = pipeline.run()"
            ],
            tags=["pipeline", "example", "tutorial"],
            status="active"
        ))
        
        # FoundryClient
        self.register(ComponentMetadata(
            name="FoundryClient",
            component_type="model",
            version="1.0.0",
            description="Central integration point for Foundry and Spark session management",
            author="Microsoft Foundry",
            source_module="src.foundry",
            class_name="FoundryClient",
            parameters={
                "workspace_id": {
                    "type": "str",
                    "required": True,
                    "description": "Foundry workspace identifier"
                },
                "api_key": {
                    "type": "str",
                    "required": True,
                    "description": "API authentication key"
                },
                "spark_session": {
                    "type": "SparkSession",
                    "required": False,
                    "description": "Optional existing Spark session"
                },
                "config": {
                    "type": "dict",
                    "required": False,
                    "description": "Configuration dictionary"
                }
            },
            examples=[
                "from src.foundry import FoundryClient",
                "client = FoundryClient(workspace_id='ws-123', api_key='key')",
                "spark = client.get_spark_session()",
                "client.close()"
            ],
            tags=["framework", "foundry", "spark"],
            status="active"
        ))
    
    def register(self, metadata: ComponentMetadata) -> None:
        """
        Register a new component in the catalog.
        
        Args:
            metadata: ComponentMetadata for the component
        
        Raises:
            ValueError: If component already registered
        """
        if metadata.name in self._components:
            raise ValueError(f"Component '{metadata.name}' already registered")
        
        self._components[metadata.name] = metadata
        
        # Update indices
        ctype = metadata.component_type
        if ctype not in self._indices["type"]:
            self._indices["type"][ctype] = []
        self._indices["type"][ctype].append(metadata.name)
        
        for tag in metadata.tags:
            if tag not in self._indices["tag"]:
                self._indices["tag"][tag] = []
            self._indices["tag"][tag].append(metadata.name)
        
        status = metadata.status
        if status not in self._indices["status"]:
            self._indices["status"][status] = []
        self._indices["status"][status].append(metadata.name)
    
    def get_component(self, name: str) -> Optional[ComponentMetadata]:
        """Get component metadata by name."""
        return self._components.get(name)
    
    def get_components(self, names: List[str]) -> List[ComponentMetadata]:
        """Get multiple components by name."""
        return [self._components[name] for name in names if name in self._components]
    
    def list_all(self) -> List[ComponentMetadata]:
        """List all registered components."""
        return list(self._components.values())
    
    def get_transforms(self) -> List[ComponentMetadata]:
        """Get all transforms."""
        names = self._indices["type"].get("transform", [])
        return [self._components[name] for name in names]
    
    def get_pipelines(self) -> List[ComponentMetadata]:
        """Get all pipelines."""
        names = self._indices["type"].get("pipeline", [])
        return [self._components[name] for name in names]
    
    def get_models(self) -> List[ComponentMetadata]:
        """Get all models."""
        names = self._indices["type"].get("model", [])
        return [self._components[name] for name in names]
    
    def list_by_tag(self, tag: str) -> List[ComponentMetadata]:
        """Get all components with a specific tag."""
        names = self._indices["tag"].get(tag, [])
        return [self._components[name] for name in names]
    
    def list_by_status(self, status: str) -> List[ComponentMetadata]:
        """Get all components with a specific status."""
        names = self._indices["status"].get(status, [])
        return [self._components[name] for name in names]
    
    def get_tags(self) -> List[str]:
        """Get all available tags."""
        return sorted(list(self._indices["tag"].keys()))
    
    def search(self, query: str) -> List[ComponentMetadata]:
        """
        Search components by name or description.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching components
        """
        query_lower = query.lower()
        results = []
        
        for component in self._components.values():
            if (query_lower in component.name.lower() or
                query_lower in component.description.lower() or
                any(query_lower in tag.lower() for tag in component.tags)):
                results.append(component)
        
        return results
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire catalog to dictionary."""
        return {
            "components": {name: meta.to_dict() for name, meta in self._components.items()},
            "indices": self._indices,
            "stats": {
                "total_components": len(self._components),
                "by_type": {t: len(names) for t, names in self._indices["type"].items()},
                "by_status": {s: len(names) for s, names in self._indices["status"].items()},
                "total_tags": len(self._indices["tag"])
            }
        }
    
    def to_json(self) -> str:
        """Convert entire catalog to JSON."""
        return json.dumps(self.to_dict(), indent=2)
    
    def print_summary(self) -> None:
        """Print a summary of the catalog."""
        print("\n" + "="*70)
        print("MICROSOFT FOUNDRY - MODEL CATALOG")
        print("="*70)
        
        stats = self.to_dict()["stats"]
        print(f"\n📦 Total Components: {stats['total_components']}")
        print(f"🏷️  Total Tags: {stats['total_tags']}")
        
        print("\n📊 By Type:")
        for ctype, count in stats["by_type"].items():
            print(f"   - {ctype.capitalize()}s: {count}")
        
        print("\n📈 By Status:")
        for status, count in stats["by_status"].items():
            print(f"   - {status.capitalize()}: {count}")
        
        print("\n🏷️  Available Tags:")
        tags = self.get_tags()
        for tag in tags:
            count = len(self._indices["tag"][tag])
            print(f"   - {tag}: {count} component(s)")
        
        print("\n" + "="*70 + "\n")
    
    def print_components(self, components: Optional[List[ComponentMetadata]] = None) -> None:
        """Print detailed component information."""
        if components is None:
            components = self.list_all()
        
        for component in components:
            print(f"\n{'='*70}")
            print(f"📦 {component.name}")
            print(f"{'='*70}")
            print(f"Type: {component.component_type}")
            print(f"Version: {component.version}")
            print(f"Status: {component.status}")
            print(f"Description: {component.description}")
            print(f"Source: {component.source_module}::{component.class_name}")
            print(f"Tags: {', '.join(component.tags)}")
            
            if component.parameters:
                print(f"\nParameters:")
                for param_name, param_info in component.parameters.items():
                    required = "required" if param_info.get("required", False) else "optional"
                    print(f"  - {param_name} ({param_info.get('type', 'any')}) [{required}]")
                    if "description" in param_info:
                        print(f"    {param_info['description']}")
            
            if component.examples:
                print(f"\nExamples:")
                for i, example in enumerate(component.examples, 1):
                    print(f"  {i}. {example}")
            
            if component.required_columns:
                print(f"Required Columns: {', '.join(component.required_columns)}")
            
            if component.output_columns:
                print(f"Output Columns: {', '.join(component.output_columns)}")


class TransformRegistry:
    """Specialized registry for data transforms."""
    
    def __init__(self, catalog: Optional[ModelCatalog] = None):
        """Initialize transform registry."""
        self.catalog = catalog or ModelCatalog()
    
    def get_all_transforms(self) -> List[ComponentMetadata]:
        """Get all available transforms."""
        return self.catalog.get_transforms()
    
    def get_transform(self, name: str) -> Optional[ComponentMetadata]:
        """Get transform by name."""
        component = self.catalog.get_component(name)
        if component and component.component_type == "transform":
            return component
        return None
    
    def list_preprocessing_transforms(self) -> List[ComponentMetadata]:
        """Get all preprocessing transforms."""
        return self.catalog.list_by_tag("preprocessing")
    
    def list_filtering_transforms(self) -> List[ComponentMetadata]:
        """Get all filtering transforms."""
        return self.catalog.list_by_tag("filtering")
    
    def list_aggregation_transforms(self) -> List[ComponentMetadata]:
        """Get all aggregation transforms."""
        return self.catalog.list_by_tag("aggregation")
    
    def print_catalog(self) -> None:
        """Print transform catalog."""
        transforms = self.get_all_transforms()
        self.catalog.print_components(transforms)

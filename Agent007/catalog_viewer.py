#!/usr/bin/env python3
"""
Model Catalog Viewer - Interactive catalog browser for the Microsoft Foundry platform.

Usage:
    python catalog_viewer.py              # Show catalog summary
    python catalog_viewer.py --transforms # Show all transforms
    python catalog_viewer.py --pipelines  # Show all pipelines
    python catalog_viewer.py --search <query>  # Search catalog
    python catalog_viewer.py --export json    # Export as JSON
"""

import sys
import json
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.catalog.registry import ModelCatalog, TransformRegistry
from src.utils.logger import get_logger

logger = get_logger(__name__)


def print_header(title: str) -> None:
    """Print formatted header."""
    width = 80
    print(f"\n{'='*width}")
    print(f"  {title:^{width-4}}")
    print(f"{'='*width}\n")


def print_component_table(components: list) -> None:
    """Print components in table format."""
    if not components:
        print("  No components found.")
        return
    
    # Calculate column widths
    name_width = max(len(c.name) for c in components) + 2
    type_width = max(len(c.component_type) for c in components) + 2
    status_width = 12
    
    # Header
    print(f"  {'Name':<{name_width}} | {'Type':<{type_width}} | {'Status':<{status_width}} | Description")
    print(f"  {'-'*name_width}-+-{'-'*type_width}-+-{'-'*status_width}-+-{'-'*40}")
    
    # Rows
    for component in components:
        desc = component.description[:37] + "..." if len(component.description) > 40 else component.description
        print(f"  {component.name:<{name_width}} | {component.component_type:<{type_width}} | {component.status:<{status_width}} | {desc}")


def show_summary(catalog: ModelCatalog) -> None:
    """Show catalog summary."""
    print_header("MICROSOFT FOUNDRY - MODEL CATALOG")
    
    catalog.print_summary()
    
    # Show example components
    print("📦 TRANSFORMS:")
    transforms = catalog.get_transforms()
    print_component_table(transforms)
    
    print("\n📋 PIPELINES:")
    pipelines = catalog.get_pipelines()
    print_component_table(pipelines)
    
    print("\n🔧 MODELS:")
    models = catalog.get_models()
    print_component_table(models)


def show_transforms(catalog: ModelCatalog) -> None:
    """Show all transforms with details."""
    print_header("AVAILABLE TRANSFORMS")
    
    transforms = catalog.get_transforms()
    
    if not transforms:
        print("  No transforms found.")
        return
    
    for i, transform in enumerate(transforms, 1):
        print(f"  {i}. {transform.name}")
        print(f"     Description: {transform.description}")
        print(f"     Version: {transform.version}")
        print(f"     Tags: {', '.join(transform.tags)}")
        if transform.parameters:
            print(f"     Parameters: {', '.join(transform.parameters.keys())}")
        if transform.examples:
            print(f"     Examples:")
            for example in transform.examples[:2]:
                print(f"       • {example}")
        print()


def show_pipelines(catalog: ModelCatalog) -> None:
    """Show all pipelines with details."""
    print_header("AVAILABLE PIPELINES")
    
    pipelines = catalog.get_pipelines()
    
    if not pipelines:
        print("  No pipelines found.")
        return
    
    for i, pipeline in enumerate(pipelines, 1):
        print(f"  {i}. {pipeline.name}")
        print(f"     Description: {pipeline.description}")
        print(f"     Version: {pipeline.version}")
        print(f"     Tags: {', '.join(pipeline.tags)}")
        if pipeline.examples:
            print(f"     Usage:")
            for example in pipeline.examples[:3]:
                print(f"       • {example}")
        print()


def show_component_detail(catalog: ModelCatalog, name: str) -> None:
    """Show detailed information about a component."""
    component = catalog.get_component(name)
    
    if not component:
        print(f"❌ Component '{name}' not found in catalog.")
        print(f"\nAvailable components: {', '.join(sorted(catalog._components.keys()))}")
        return
    
    print_header(f"COMPONENT DETAILS: {component.name}")
    
    print(f"  Type: {component.component_type}")
    print(f"  Version: {component.version}")
    print(f"  Status: {component.status}")
    print(f"  Author: {component.author}")
    print(f"  Created: {component.created_date}")
    print()
    
    print(f"  Description:")
    print(f"  {component.description}")
    print()
    
    print(f"  Source:")
    print(f"  Module: {component.source_module}")
    print(f"  Class: {component.class_name}")
    print()
    
    if component.tags:
        print(f"  Tags: {', '.join(component.tags)}")
        print()
    
    if component.parameters:
        print(f"  Parameters:")
        for param_name, param_info in component.parameters.items():
            required = "✓ required" if param_info.get("required", False) else "optional"
            param_type = param_info.get("type", "any")
            print(f"    • {param_name} ({param_type}) [{required}]")
            if "description" in param_info:
                print(f"      {param_info['description']}")
            if "example" in param_info:
                print(f"      Example: {param_info['example']}")
        print()
    
    if component.examples:
        print(f"  Usage Examples:")
        for i, example in enumerate(component.examples, 1):
            print(f"    {i}. {example}")
        print()
    
    if component.required_columns:
        print(f"  Required Columns: {', '.join(component.required_columns)}")
        print()
    
    if component.output_columns:
        print(f"  Output Columns: {', '.join(component.output_columns)}")
        print()


def search_catalog(catalog: ModelCatalog, query: str) -> None:
    """Search catalog for components."""
    print_header(f"SEARCH RESULTS FOR: '{query}'")
    
    results = catalog.search(query)
    
    if not results:
        print(f"  ❌ No components found matching '{query}'")
        return
    
    print(f"  Found {len(results)} component(s):\n")
    print_component_table(results)
    
    print(f"\n  Use 'python catalog_viewer.py --detail <name>' for details.")


def export_catalog(catalog: ModelCatalog, format_type: str) -> None:
    """Export catalog in specified format."""
    print_header(f"EXPORTING CATALOG AS {format_type.upper()}")
    
    if format_type == "json":
        output = catalog.to_json()
        print(output)
    else:
        print(f"❌ Unsupported format: {format_type}")


def list_tags(catalog: ModelCatalog) -> None:
    """List all available tags."""
    print_header("AVAILABLE TAGS")
    
    tags = catalog.get_tags()
    
    print("  Tags and component count:")
    print()
    
    for tag in tags:
        components = catalog.list_by_tag(tag)
        comp_names = ", ".join([c.name for c in components])
        print(f"  • {tag:<20} ({len(components)} components)")
        print(f"    {comp_names}")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Microsoft Foundry Model Catalog Viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python catalog_viewer.py                    # Show summary
  python catalog_viewer.py --transforms       # Show all transforms
  python catalog_viewer.py --pipelines        # Show all pipelines
  python catalog_viewer.py --search cleaning  # Search for components
  python catalog_viewer.py --detail CleaningTransform  # Show details
  python catalog_viewer.py --tags             # List all tags
  python catalog_viewer.py --export json      # Export as JSON
        """)
    
    parser.add_argument(
        "--transforms",
        action="store_true",
        help="Show all transforms"
    )
    parser.add_argument(
        "--pipelines",
        action="store_true",
        help="Show all pipelines"
    )
    parser.add_argument(
        "--models",
        action="store_true",
        help="Show all models"
    )
    parser.add_argument(
        "--search",
        type=str,
        metavar="QUERY",
        help="Search catalog for components"
    )
    parser.add_argument(
        "--detail",
        type=str,
        metavar="NAME",
        help="Show detailed information about a component"
    )
    parser.add_argument(
        "--tags",
        action="store_true",
        help="List all available tags"
    )
    parser.add_argument(
        "--export",
        type=str,
        choices=["json"],
        help="Export catalog in specified format"
    )
    
    args = parser.parse_args()
    
    # Initialize catalog
    catalog = ModelCatalog()
    
    try:
        if args.transforms:
            show_transforms(catalog)
        elif args.pipelines:
            show_pipelines(catalog)
        elif args.models:
            models = catalog.get_models()
            print_header("AVAILABLE MODELS")
            print_component_table(models)
        elif args.search:
            search_catalog(catalog, args.search)
        elif args.detail:
            show_component_detail(catalog, args.detail)
        elif args.tags:
            list_tags(catalog)
        elif args.export:
            export_catalog(catalog, args.export)
        else:
            show_summary(catalog)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

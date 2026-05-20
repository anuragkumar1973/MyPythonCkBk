"""
Simple Demo - Microsoft Foundry Project Demo Without Spark
This demonstrates the project structure without requiring Java/Spark

Features:
- Loads configuration from .env file
- Displays Azure credentials (Subscription, Resource Group, Storage Account)
- Shows "None" for missing or unconfigured values
- Demonstrates complete configuration management
"""

import sys
import os
from pathlib import Path

# Add project root to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.utils.logger import get_logger
from src.utils.config import Config


def display_azure_credentials(config: Config) -> None:
    """
    Display Azure credentials from configuration.
    
    Shows "None" for missing or unconfigured values.
    
    Args:
        config: Configuration object
    """
    subscription = config.azure_subscription_id or "None"
    resource_group = config.azure_resource_group or "None"
    storage_account = config.azure_storage_account or "None"
    
    print("\n" + "=" * 70)
    print("AZURE CREDENTIALS FROM .env FILE")
    print("=" * 70)
    print(f"Subscription ID:    {subscription}")
    print(f"Resource Group:     {resource_group}")
    print(f"Storage Account:    {storage_account}")
    print("=" * 70 + "\n")
    
    return subscription, resource_group, storage_account


def main():
    """Run a simple demo of the Foundry project."""
    
    # Initialize logger
    logger = get_logger(__name__, level="INFO")
    
    logger.info("=" * 70)
    logger.info("Microsoft Foundry Project - Demo")
    logger.info("=" * 70)
    
    try:
        # Load configuration from .env file
        logger.info("Loading configuration from .env file...")
        config = Config()
        
        # Display Azure credentials
        subscription, resource_group, storage_account = display_azure_credentials(config)
        
        # Log Azure credentials
        logger.info(f"Azure Subscription ID: {subscription}")
        logger.info(f"Azure Resource Group: {resource_group}")
        logger.info(f"Azure Storage Account: {storage_account}")
        
        # Display other configuration settings
        logger.info("\n" + "=" * 70)
        logger.info("APPLICATION CONFIGURATION")
        logger.info("=" * 70)
        logger.info(f"Environment: {config.environment}")
        logger.info(f"Log Level: {config.log_level}")
        logger.info(f"Debug Mode: {config.debug}")
        logger.info(f"Foundry Workspace: {config.foundry_workspace or 'None'}")
        logger.info(f"Spark Master: {config.spark_master}")
        
        # Show data configuration
        logger.info("\n" + "=" * 70)
        logger.info("DATA CONFIGURATION")
        logger.info("=" * 70)
        logger.info(f"Data Raw Path: {config.data_raw_path}")
        logger.info(f"Data Processed Path: {config.data_processed_path}")
        logger.info(f"Checkpoint Path: {config.checkpoint_path}")
        logger.info(f"Batch Size: {config.batch_size}")
        logger.info(f"Max Retries: {config.max_retries}")
        
        logger.info("\n" + "=" * 70)
        logger.info("✓ Configuration loaded successfully!")
        logger.info("=" * 70)
        
        # Show configuration status
        if subscription != "None" and resource_group != "None":
            logger.info("✓ Azure credentials are configured and ready!")
        else:
            logger.warning("⚠ Some Azure credentials are missing or not set in .env file")
            logger.warning("To configure, edit your .env file with valid values:")
            logger.warning("  - AZURE_SUBSCRIPTION_ID")
            logger.warning("  - AZURE_RESOURCE_GROUP")
            logger.warning("  - AZURE_STORAGE_ACCOUNT")
        
        # Show next steps
        logger.info("\n" + "=" * 70)
        logger.info("NEXT STEPS")
        logger.info("=" * 70)
        logger.info("1. Configure .env file with your Azure credentials")
        logger.info("2. Install Java: brew install openjdk@11")
        logger.info("3. Run the full pipeline: python run_pipeline.py")
        logger.info("4. Run tests: pytest tests/ -v")
        logger.info("5. Create custom transforms in src/transforms/")
        logger.info("=" * 70 + "\n")
        
        return 0
        
    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

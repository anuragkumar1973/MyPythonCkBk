"""
Simple Demo - Microsoft Foundry Project Demo Without Spark
This demonstrates the project structure without requiring Java/Spark
"""

import sys
import os

from src.utils.config import Config

config = Config()
print(f"Subscription: {config.azure_subscription_id}")
print(f"Resource Group: {config.azure_resource_group}")
print(f"Storage Account: {config.azure_storage_account}")

# Add project root to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.utils.logger import get_logger
from src.utils.config import load_config

def main():
    """Run a simple demo of the Foundry project."""
    
    # Initialize logger
    logger = get_logger(__name__, level="INFO")
    
    logger.info("=" * 70)
    logger.info("Microsoft Foundry Project - Demo")
    logger.info("=" * 70)
    
    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        logger.info(f"Environment: {config.environment}")
        logger.info(f"Log Level: {config.log_level}")
        logger.info(f"Foundry Workspace: {config.foundry_workspace or 'Not set'}")
        logger.info(f"Spark Master: {config.spark_master}")
        
        # Show configuration
        logger.info("Configuration loaded successfully!")
        logger.info(f"Data Raw Path: {config.data_raw_path}")
        logger.info(f"Data Processed Path: {config.data_processed_path}")
        logger.info(f"Batch Size: {config.batch_size}")
        logger.info(f"Max Retries: {config.max_retries}")
        
        logger.info("=" * 70)
        logger.info("✓ Project is working correctly!")
        logger.info("=" * 70)
        
        # Show next steps
        logger.info("\nNext Steps:")
        logger.info("1. Install Java: brew install openjdk@11")
        logger.info("2. Run the full pipeline: python run_pipeline.py")
        logger.info("3. Run tests: pytest tests/ -v")
        logger.info("4. Create custom transforms in src/transforms/")
        
        return 0
        
    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

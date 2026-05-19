"""
Sample Data Pipeline
"""

import logging
from typing import Optional, Dict, Any
from pyspark.sql import DataFrame, SparkSession
from src.foundry import FoundryClient
from src.transforms import CleaningTransform, FilterTransform, AggregationTransform


class SamplePipeline:
    """
    Sample data pipeline demonstrating common patterns.
    
    This pipeline:
    1. Reads sample data
    2. Applies cleaning transform
    3. Applies filtering
    4. Writes processed data
    """
    
    def __init__(
        self,
        foundry_client: FoundryClient,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize pipeline.
        
        Args:
            foundry_client: Foundry client instance
            config: Pipeline configuration
        """
        self.foundry_client = foundry_client
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
    
    def create_sample_data(self) -> DataFrame:
        """Create sample DataFrame for demonstration."""
        self.logger.info("Creating sample data")
        
        spark = self.foundry_client.get_spark_session()
        
        data = [
            (1, "Alice", 25, 50000),
            (2, "Bob", 30, 60000),
            (3, "Charlie", 28, 55000),
            (4, "Diana", 35, 75000),
            (5, "Eve", 29, 65000),
        ]
        
        schema = ["id", "name", "age", "salary"]
        df = spark.createDataFrame(data, schema=schema)
        
        self.logger.info(f"Created sample data with {df.count()} rows")
        return df
    
    def run(self) -> DataFrame:
        """
        Execute the pipeline.
        
        Returns:
            Processed DataFrame
        """
        try:
            self.logger.info("Starting SamplePipeline")
            
            # Create sample data
            df = self.create_sample_data()
            self.logger.info(f"Input: {df.count()} rows")
            
            # Apply transforms
            cleaning = CleaningTransform("cleaning")
            df = cleaning(df)
            self.logger.info(f"After cleaning: {df.count()} rows")
            
            # Filter high earners
            filter_config = {
                "condition": "salary > 55000"
            }
            filtering = FilterTransform("salary_filter", config=filter_config)
            df = filtering(df)
            self.logger.info(f"After filtering: {df.count()} rows")
            
            # Show results
            self.logger.info("Pipeline Results:")
            df.show()
            
            self.logger.info("SamplePipeline completed successfully")
            return df
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise


def main():
    """Main entry point for sample pipeline."""
    import os
    from src.utils.config import load_config
    from src.utils.logger import get_logger
    
    # Load configuration
    config = load_config()
    logger = get_logger(__name__, level=config.log_level)
    
    try:
        # Create Foundry client
        foundry_client = FoundryClient(
            workspace_id=config.foundry_workspace or "sample-workspace",
            api_key=config.foundry_api_key or "sample-key",
            config=config.to_dict()
        )
        
        # Run pipeline
        pipeline = SamplePipeline(foundry_client, config=config.to_dict())
        result = pipeline.run()
        
    except Exception as e:
        logger.error(f"Failed to run pipeline: {e}", exc_info=True)
        raise
    finally:
        # Cleanup
        if 'foundry_client' in locals():
            foundry_client.close()


if __name__ == "__main__":
    main()

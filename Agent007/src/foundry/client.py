"""
Foundry Client Module - Central integration point for Microsoft Foundry
"""

from typing import Optional, Dict, Any
import logging
from pyspark.sql import SparkSession


class FoundryClient:
    """
    Main Foundry client for data operations and pipeline management.
    
    Attributes:
        workspace_id (str): Foundry workspace identifier
        api_key (str): API key for authentication
        spark_session (SparkSession): Spark session instance
    """
    
    def __init__(
        self,
        workspace_id: str,
        api_key: str,
        spark_session: Optional[SparkSession] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Foundry client.
        
        Args:
            workspace_id: Foundry workspace identifier
            api_key: API key for authentication
            spark_session: Existing Spark session (optional)
            config: Configuration dictionary (optional)
        """
        self.workspace_id = workspace_id
        self.api_key = api_key
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize or use provided Spark session
        self.spark_session = spark_session or self._create_spark_session()
    
    def _create_spark_session(self) -> SparkSession:
        """Create and configure a Spark session."""
        self.logger.info("Creating Spark session...")
        
        session = SparkSession.builder \
            .appName("FoundryPipeline") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()
        
        self.logger.info("Spark session created successfully")
        return session
    
    def get_spark_session(self) -> SparkSession:
        """Get the Spark session instance."""
        return self.spark_session
    
    def close(self) -> None:
        """Close the Spark session."""
        if self.spark_session:
            self.logger.info("Closing Spark session...")
            self.spark_session.stop()
            self.logger.info("Spark session closed")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
    
    def __repr__(self) -> str:
        """String representation of FoundryClient."""
        return (
            f"FoundryClient(workspace_id='{self.workspace_id}', "
            f"spark_app_name='{self.spark_session.sparkContext.appName}')"
        )


__all__ = ["FoundryClient"]

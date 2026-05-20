"""
Configuration Management - Load and manage application settings
"""

import os
from typing import Any, Optional, Dict
from pathlib import Path
import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration using Pydantic."""
    
    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Azure
    azure_subscription_id: Optional[str] = Field(default=None, env="AZURE_SUBSCRIPTION_ID")
    azure_resource_group: Optional[str] = Field(default=None, env="AZURE_RESOURCE_GROUP")
    azure_storage_account: Optional[str] = Field(default=None, env="AZURE_STORAGE_ACCOUNT")
    azure_storage_key: Optional[str] = Field(default=None, env="AZURE_STORAGE_KEY")
    
    # Foundry
    foundry_workspace: Optional[str] = Field(default=None, env="FOUNDRY_WORKSPACE")
    foundry_api_key: Optional[str] = Field(default=None, env="FOUNDRY_API_KEY")
    endpoint: Optional[str] = Field(default=None, env="ENDPOINT")
    
    # Spark
    spark_master: str = Field(default="local[*]", env="SPARK_MASTER")
    spark_driver_memory: str = Field(default="4g", env="SPARK_DRIVER_MEMORY")
    spark_executor_memory: str = Field(default="2g", env="SPARK_EXECUTOR_MEMORY")
    
    # Data paths
    data_raw_path: str = Field(default="./data/raw", env="DATA_RAW_PATH")
    data_processed_path: str = Field(default="./data/processed", env="DATA_PROCESSED_PATH")
    checkpoint_path: str = Field(default="./checkpoints", env="CHECKPOINT_PATH")
    
    # Pipeline settings
    batch_size: int = Field(default=1000, env="BATCH_SIZE")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    retry_delay: int = Field(default=5, env="RETRY_DELAY")
    timeout: int = Field(default=3600, env="TIMEOUT")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> "Config":
        """
        Load configuration from YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            Config instance
        """
        with open(yaml_path, "r") as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.dict()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return getattr(self, key, default)


def load_config(env_file: Optional[str] = None) -> Config:
    """
    Load configuration from environment variables and .env file.
    
    Args:
        env_file: Path to .env file (optional)
        
    Returns:
        Config instance
    """
    if env_file and Path(env_file).exists():
        os.environ["ENV_FILE"] = env_file
    
    return Config()

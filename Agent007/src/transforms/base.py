"""
Data Transformations - Base transform class and common utilities
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
from pyspark.sql import DataFrame
import logging


class BaseTransform(ABC):
    """
    Abstract base class for all data transformations.
    
    All transform implementations should inherit from this class
    and implement the transform() method.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize transform.
        
        Args:
            name: Transform name
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """
        Apply transformation to DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Transformed DataFrame
        """
        pass
    
    def validate_input(self, df: DataFrame, required_columns: list) -> None:
        """
        Validate input DataFrame has required columns.
        
        Args:
            df: Input DataFrame
            required_columns: List of required column names
            
        Raises:
            ValueError: If required columns are missing
        """
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"Missing required columns for {self.name}: {missing_columns}"
            )
    
    def __call__(self, df: DataFrame) -> DataFrame:
        """Allow transform to be called as a function."""
        self.logger.info(f"Executing {self.name}")
        result = self.transform(df)
        self.logger.info(f"Completed {self.name}: {result.count()} rows")
        return result


class CleaningTransform(BaseTransform):
    """Data cleaning and validation transform."""
    
    def transform(self, df: DataFrame) -> DataFrame:
        """Remove null values and duplicates."""
        self.logger.info(f"Cleaning data in {self.name}")
        
        # Remove duplicates
        df = df.dropDuplicates()
        
        # Remove rows with all null values
        df = df.dropna(how="all")
        
        return df


class FilterTransform(BaseTransform):
    """Filter data based on conditions."""
    
    def transform(self, df: DataFrame) -> DataFrame:
        """Apply filter condition from config."""
        condition = self.config.get("condition")
        if not condition:
            self.logger.warning(f"No filter condition provided for {self.name}")
            return df
        
        self.logger.info(f"Applying filter: {condition}")
        return df.filter(condition)


class AggregationTransform(BaseTransform):
    """Aggregate data based on configuration."""
    
    def transform(self, df: DataFrame) -> DataFrame:
        """Apply aggregation."""
        group_by_cols = self.config.get("group_by", [])
        agg_dict = self.config.get("aggregations", {})
        
        if not group_by_cols or not agg_dict:
            self.logger.warning(f"No aggregation config for {self.name}")
            return df
        
        self.logger.info(f"Aggregating by: {group_by_cols}")
        return df.groupBy(*group_by_cols).agg(agg_dict)


"""
Tests - Unit tests for transforms
"""

import pytest
from pyspark.sql import SparkSession
from src.transforms import CleaningTransform, FilterTransform


@pytest.fixture
def spark():
    """Fixture for Spark session."""
    session = SparkSession.builder \
        .appName("test") \
        .master("local[1]") \
        .getOrCreate()
    yield session
    session.stop()


def test_cleaning_transform_removes_duplicates(spark):
    """Test that CleaningTransform removes duplicate rows."""
    data = [
        (1, "Alice", 25),
        (1, "Alice", 25),  # Duplicate
        (2, "Bob", 30),
    ]
    schema = ["id", "name", "age"]
    df = spark.createDataFrame(data, schema=schema)
    
    transform = CleaningTransform("test_cleaning")
    result = transform.transform(df)
    
    assert result.count() == 2


def test_filter_transform_applies_condition(spark):
    """Test that FilterTransform applies filter condition."""
    data = [
        (1, "Alice", 25),
        (2, "Bob", 30),
        (3, "Charlie", 28),
    ]
    schema = ["id", "name", "age"]
    df = spark.createDataFrame(data, schema=schema)
    
    config = {"condition": "age > 27"}
    transform = FilterTransform("test_filter", config=config)
    result = transform.transform(df)
    
    assert result.count() == 2


def test_filter_transform_without_config(spark):
    """Test that FilterTransform handles missing config."""
    data = [(1, "Alice", 25), (2, "Bob", 30)]
    schema = ["id", "name", "age"]
    df = spark.createDataFrame(data, schema=schema)
    
    transform = FilterTransform("test_filter")
    result = transform.transform(df)
    
    assert result.count() == 2  # No filter applied


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""
Microsoft Foundry Project - Package Initialization
"""

__version__ = "1.0.0"
__author__ = "Data Engineering Team"
__description__ = "Microsoft Foundry Data Engineering and ML Pipeline Project"

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == "FoundryClient":
        from src.foundry import FoundryClient
        return FoundryClient
    elif name == "get_logger":
        from src.utils.logger import get_logger
        return get_logger
    elif name == "Config":
        from src.utils.config import Config
        return Config
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "FoundryClient",
    "get_logger",
    "Config",
]

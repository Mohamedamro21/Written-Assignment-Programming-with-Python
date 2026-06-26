"""
models package

This package contains all core modules for the Ideal Function Project:
- Data loading
- Database management
- Function selection (Least Squares)
- Mapping logic
- Visualization
- Custom exceptions
"""

from .base_loader import BaseLoader
from .data_loader import DataLoader
from .database import DatabaseManager
from .function_selector import FunctionSelector
from .mapper import FunctionMapper
from .visualizer import Visualizer
from .exceptions import (
    DatabaseError,
    FunctionSelectionError,
    MappingError,
    VisualizationError,
    DataLoadingError
)

__all__ = [
    "BaseLoader",
    "DataLoader",
    "DatabaseManager",
    "FunctionSelector",
    "FunctionMapper",
    "Visualizer",
    "DatabaseError",
    "FunctionSelectionError",
    "MappingError",
    "VisualizationError",
    "DataLoadingError",
]
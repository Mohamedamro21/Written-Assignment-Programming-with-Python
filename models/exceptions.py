"""
exceptions.py

Custom exception classes used throughout the Ideal Function Project.

Author: Mohamed Amro
"""


class DataLoadingError(Exception):
    """
    Raised when a CSV file cannot be loaded or is invalid.
    """

    def __init__(self, message="Error loading CSV file."):
        super().__init__(message)


class DatabaseError(Exception):
    """
    Raised when a database operation fails.
    """

    def __init__(self, message="Database operation failed."):
        super().__init__(message)


class FunctionSelectionError(Exception):
    """
    Raised when no suitable ideal function can be selected.
    """

    def __init__(self, message="Unable to select an ideal function."):
        super().__init__(message)


class MappingError(Exception):
    """
    Raised when a test point cannot be mapped to any ideal function.
    """

    def __init__(self, message="Unable to map the test point."):
        super().__init__(message)


class VisualizationError(Exception):
    """
    Raised when visualization cannot be generated.
    """

    def __init__(self, message="Visualization failed."):
        super().__init__(message)
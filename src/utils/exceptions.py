
"""Custom application exceptions."""


class DataAnalystError(Exception):
    """Base exception for the Data Analyst Agent application."""


class DatasetError(DataAnalystError):
    """Raised when a dataset cannot be loaded or validated."""


class DataValidationError(DataAnalystError):
    """Raised when dataset contents fail validation."""


class AnalysisError(DataAnalystError):
    """Raised when an analysis operation fails."""


class DatabaseError(DataAnalystError):
    """Raised when a database operation fails."""


class ReportExportError(DataAnalystError):
    """Raised when a report cannot be exported."""

class QpdfException(Exception):
    """Base class for all qpdf-related errors."""


class QpdfFileNotFoundError(QpdfException, FileNotFoundError):
    """Raised when a required qpdf input file does not exist."""


class QpdfFileExistsError(QpdfException, FileExistsError):
    """Raised when qpdf would overwrite an existing file."""

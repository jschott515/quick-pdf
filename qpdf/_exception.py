import pymupdf


class QpdfException(Exception):
    """Base class for all qpdf-related errors."""


class QpdfFileNotFoundError(QpdfException, FileNotFoundError):
    """Raised when a required qpdf input file does not exist."""


class QpdfFileExistsError(QpdfException, FileExistsError):
    """Raised when qpdf would overwrite an existing file."""


class QpdfFileDataError(QpdfException, pymupdf.FileDataError):  # type: ignore[name-defined]
    """Raised when qpdf cannot read a file."""

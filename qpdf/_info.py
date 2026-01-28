import importlib.metadata
import importlib.resources

PACKAGE = "quick-pdf"

try:
    AUTHOR, AUTHOR_EMAIL = importlib.metadata.metadata(PACKAGE).get("Author-email", "").split()

    VERSION_MAJOR, VERSION_MINOR, VERSION_REV = importlib.metadata.version(PACKAGE).split(".")
    VERSION = f"v{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_REV}"

    _, HOMEPAGE = importlib.metadata.metadata(PACKAGE).get("Project-URL", "").split()

    ICON = importlib.resources.files("qpdf.gui.assets").joinpath("QuickPdf.ico")
except:
    raise RuntimeError(f"Verify that {PACKAGE} is installed prior to running... (pip install -e .)")

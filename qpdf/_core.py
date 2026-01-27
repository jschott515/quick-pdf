import pathlib

import pymupdf

from ._exception import QpdfFileExistsError


def pdf_save(pdf: pymupdf.Document, out: pathlib.Path, force: bool = False) -> None:
    if out.exists() and not force:
        raise QpdfFileExistsError("Output file already exists and force is not set!")
    pdf.save(out)
    pdf.close()

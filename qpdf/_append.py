import pathlib
import typing

import pymupdf

from ._exception import QpdfFileNotFoundError


def pdf_append(files: typing.Sequence[pathlib.Path]) -> pymupdf.Document:
    pdf = pymupdf.open()

    missing_files = [file for file in files if not file.exists()]
    if missing_files:
        raise QpdfFileNotFoundError(
            f"Could not find files: `{'`, `'.join([file.as_posix() for file in missing_files])}`"
        )

    for file in files:
        pdf.insert_pdf(pymupdf.open(file.as_posix()))

    return pdf

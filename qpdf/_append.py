import pathlib
import typing

import pymupdf

from ._exception import QpdfFileDataError, QpdfFileNotFoundError


def pdf_append(files: typing.Sequence[pathlib.Path]) -> pymupdf.Document:
    pdf = pymupdf.open()

    missing_files = [file for file in files if not file.exists()]
    if missing_files:
        raise QpdfFileNotFoundError(
            f"Could not find files: `{'`, `'.join([file.as_posix() for file in missing_files])}`"
        )

    for file in files:
        try:
            pdf.insert_pdf(pymupdf.open(file.as_posix()))
        except pymupdf.FileDataError:  # type: ignore[attr-defined]
            raise QpdfFileDataError(f"Failed to read file `{file.as_posix()}`")

    return pdf

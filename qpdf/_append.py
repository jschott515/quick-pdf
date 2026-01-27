import pathlib
import typing

import pypdf

from ._exception import QpdfFileNotFoundError


def pdf_append(files: typing.Sequence[pathlib.Path]) -> pypdf.PdfWriter:
    writer = pypdf.PdfWriter()

    missing_files = [file for file in files if not file.exists()]
    if missing_files:
        raise QpdfFileNotFoundError(
            f"Could not find files: `{'`, `'.join([file.as_posix() for file in missing_files])}`"
        )

    for file in files:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)

    return writer

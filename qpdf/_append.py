import pathlib
import typing

import pypdf

from ._exception import QpdfFileExistsError, QpdfFileNotFoundError


def pdf_append(files: typing.Sequence[pathlib.Path], out: pathlib.Path, force: bool = False) -> None:
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

    if out.exists() and not force:
        raise QpdfFileExistsError("Output file already exists and force is not set!")

    with open(out, "wb") as f:
        writer.write(f)

import pathlib

import pypdf

from ._exception import QpdfFileExistsError


def pdf_save(writer: pypdf.PdfWriter, out: pathlib.Path, force: bool = False) -> None:
    if out.exists() and not force:
        raise QpdfFileExistsError("Output file already exists and force is not set!")

    with open(out, "wb") as f:
        writer.write(f)

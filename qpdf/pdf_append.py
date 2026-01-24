"""
Quick PDF pdf-append tool.
Combine multiple PDF files into one!
"""

import argparse
import pathlib
import sys
import typing

import pypdf

import qpdf

DEFAULT_OUT = pathlib.Path("qpdf_merged.pdf")


def main() -> int:
    cfg = parse_args()
    writer = pypdf.PdfWriter()

    missing_files = [file for file in cfg.FILES if not file.exists()]
    if missing_files:
        print(f"Could not find files: `{'`, `'.join([file.as_posix() for file in missing_files])}`")
        return 1

    for file in cfg.FILES:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)

    if cfg.out.exists() and not cfg.force:
        print("Output file already exists and force is not set!")
        return 1

    with open(cfg.out, "wb") as f:
        writer.write(f)
    return 0


class LocalArgs(typing.Protocol):
    FILES: typing.Sequence[pathlib.Path]
    out: pathlib.Path
    force: bool


class LocalParser(argparse.ArgumentParser):
    def error(self, message: str) -> typing.Never:
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def parse_args() -> LocalArgs:
    parser = LocalParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("FILES", type=pathlib.Path, nargs="+", help="PDF Files to append.")
    parser.add_argument("-o", "--out", type=pathlib.Path, default=DEFAULT_OUT, help="Output file path.")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output file?")
    cfg = parser.parse_args()
    return cfg


if __name__ == "__main__":
    sys.exit(main())

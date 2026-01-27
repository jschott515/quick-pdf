"""
Quick PDF pdf-append tool.
Combine multiple PDF files into one!
"""

import argparse
import pathlib
import sys
import typing

import qpdf

DEFAULT_OUT = pathlib.Path("qpdf_merged.pdf")


def main() -> None:
    cfg = parse_args()
    try:
        result = qpdf.pdf_append(cfg.FILES)
        qpdf.pdf_save(result, cfg.out, cfg.force)
    except qpdf.QpdfException as e:
        print(e)
        sys.exit(1)


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
    main()

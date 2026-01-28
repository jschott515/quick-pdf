# Quick PDF
Simple PDF Utilities

## Install
**Requires python 3.14.**

QuickPdf and its command-line tools can be installed with pip.
By default, executables are usually installed under `C:\Users\<Username>\AppData\Local\Programs\Python\PythonXX\Scripts\` unless otherwise configured by the user.
This document assumes that this directory is on the user's PATH.

Install with pip and git:
```bash
pip install git+https://github.com/jschott515/quick-pdf.git
```

For development:
```bash
git clone https://github.com/jschott515/quick-pdf.git
cd quick-pdf
pip install -e .[dev]
```

## QuickPdf GUI
Launch from the command line (assumes that quick-pdf was [installed with pip](/README.md#install)):
```bash
QuickPdf
```

*OR*

Create a standalone executable with pyinstaller:
```bash
cd quick-pdf
pyinstaller --onefile --name QuickPdf --noconsole --copy-metadata quick-pdf --add-data "qpdf/gui/assets;qpdf/gui/assets" --icon .\qpdf\gui\assets\QuickPdf.ico .\qpdf\gui\main.py
```

*OR*

Download `QuickPdf.exe` from the [latest release](https://github.com/jschott515/quick-pdf/releases/latest)!

### Home
![image](/docs/images/QuickPdfHome.png)

### Pdf Append
![image](/docs/images/QuickPdf_PdfAppend_AddDocuments.png)
![image](/docs/images/QuickPdf_PdfAppend_Preview.png)

## CLI Tools
The following assumes that quick-pdf was [installed with pip](/README.md#install).

### pdf-append
```bash
> pdf-append --help
```
```
usage: pdf-append
       [-h] [-o OUT] [-f] FILES [FILES ...]

Quick PDF pdf-append tool.
Combine multiple PDF files into one!

positional arguments:
  FILES          PDF Files to append.

options:
  -h, --help     show this help message and exit
  -o, --out OUT  Output file path.
  -f, --force    Overwrite output file?
```

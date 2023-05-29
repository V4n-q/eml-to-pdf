# eml to pdf

Python Script to convert EML files into PDF files. Can convert EML files from specific directory and its subdirectories. The converted files are saved inside "pdf files" directory.

# Requirements

- Run `pip install -r Requirements.txt`
- Install `wkhtmltopdf` from [wkhtmltopdf official site](https://wkhtmltopdf.org/downloads.html).
or
- Visit [wkhtmltopdf github](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)

> __Note__: Add the bin directory of the wkhtmltopdf in your PATH (Environment Variable) !

# Usage

- `py main.py`

  Select Conversion Type when prompted and enter the file path or directory path.

## Conversion Type

- Single
- Bulk

### Single Conversion :

Convert only one EML file at one run. Enter file path when prompted.

### Bulk Conversion :

Convert multiple EML file at one run. Enter folder path when prompted.
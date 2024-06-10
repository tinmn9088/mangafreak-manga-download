# Mangafreak Manga Download

Download manga from `mangafreak.me` as PDF files.

## Launch

Setup ImageMagick because script calls `convert * out.pdf` to generate PDF.

Install required packages:

`pip install argparse beautifulsoup4 requests`

Download chapter list page HTML and run:

`python run.py <chapter_list_html_path> -a <author> -t <title>`

Optional command line arguments:

| Name  |Description                                                               |
|:---   |:---                                                                      |
| `-ch` | Maximum number of chapters in a PDF file (_15_ by default).              |
| `-a`  | Manga **author** used in PDF-file names (_'Unknown'_ by default).        |
| `-t`  | Manga **title** used in PDF-file names (_title url version_ by default). |
| `-v`  | Print ImageMagick output.                                                |
| `-st` | Chapter to start from.                                                   |
# Mangafreak Manga Download

Download manga from `mangafreak.me` as PDF files.

## Launch

Install required packages:

`pip install argparse beautifulsoup4`

Download chapter list page HTML and run:

`python run.py <chapter_list_html_path>`

Optional command line arguments:

| Name  |Description                                                   |
|:---   |:---                                                          |
| `-ch` | Maximum number of chapters in one PDF file (default **15**). |

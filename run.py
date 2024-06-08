from cli_utils import parse_args


args = parse_args()

print(
    f'Running with args:',
    f' * manga title: "{args.title}"',
    f' * chapters per file: {args.chapters_per_file}',
    sep='\n'
)

print('Not implemented')

# TODO: generate url of the manga page, retrieve HTML and parse the list of chapters

# TODO: generate urls of images and download them

# TODO: assemble images in PDF

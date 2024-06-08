from argparse import ArgumentParser


def parse_args():
    """
    Runs ArgumentParser and returns namespace with properties:
    * title
    * chapters_per_file
    """

    parser = ArgumentParser(
        prog='python run.py',
        description='Download manga from "mangafreak.me" and convert it to PDF.'
    )

    parser.add_argument('-t', '--title', required=True)
    parser.add_argument('-ch', '--chapters-per-file', type=int, default=15)

    return parser.parse_args()

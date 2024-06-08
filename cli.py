from argparse import ArgumentParser
from settings import Settings


class ArgumentService:

    @staticmethod
    def get_settings() -> Settings:
        """
        Read command line arguments.
        """

        parser = ArgumentParser(
            prog='python run.py',
            description='Download manga from "mangafreak.me" and convert it to PDF.'
        )

        # command line arguments
        parser.add_argument('path')
        parser.add_argument('-ch', '--chapters-per-file', type=int, default=15)

        namespace = parser.parse_args()

        return Settings(
            namespace.path,
            namespace.chapters_per_file
        )

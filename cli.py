from argparse import ArgumentParser
from settings import Settings


class ArgumentService:

    @staticmethod
    def get_settings() -> Settings:
        '''
        Read command line arguments.
        '''

        parser = ArgumentParser(
            prog='python run.py',
            description='Download manga from "mangafreak.me" and convert it to PDF.'
        )

        # command line arguments
        parser.add_argument('path')
        parser.add_argument('-ch', '--chapters-per-file', type=int, default=15)
        parser.add_argument('-a', '--author', type=str, default='Unknown')
        parser.add_argument('-t', '--title', type=str, default=None)
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-st', '--chapter-to-start-from', type=str, default=None)

        namespace = parser.parse_args()

        return Settings(
            namespace.path,
            namespace.chapters_per_file,
            namespace.author,
            namespace.title,
            namespace.verbose,
            namespace.chapter_to_start_from
        )


class MessageService:

    WARN_PREFIX = '[\033[33mWARN\033[0m]'

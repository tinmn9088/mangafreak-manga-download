from bs4 import BeautifulSoup
import re
import requests
import os


class MangafreakService:

    TITLE_SELECTOR = '.manga_series_data h1'

    CHAPTER_LIST_SELECTOR = '.manga_series_list_section tbody'

    DOWNLOADS_DIRECTORY = 'downloads'

    DOWNLOAD_CHUNK_SIZE_BYTES = 1024 * 1024

    @classmethod
    def parse_html(cls, chapter_list_html_path: str) -> tuple[str, list[str]]:
        '''
        Get manga title and list of chapters.
        '''

        with open(chapter_list_html_path, mode='r') as html_file:
            html = BeautifulSoup(html_file, 'html.parser')

        # parse manga title
        title = html.select_one(cls.TITLE_SELECTOR).text

        # get <tbody>
        chapter_list_tbody = html.select_one(cls.CHAPTER_LIST_SELECTOR)

        chapter_numbers = []

        # iterate through <tbody>
        for chapter_list_tr in chapter_list_tbody:

            # elements containing chapter names are assumed to be <tr>
            if chapter_list_tr.name != 'tr':
                continue

            # get the first <td> (contains 'Chapter <number> ...' text)
            chapter_name = chapter_list_tr.find_next('td').text

            # extract chapter number
            if match := re.search('^Chapter ([^\\s]+)', chapter_name):
                chapter_numbers.append(match.group(1))

        return (title, chapter_numbers)

    @staticmethod
    def get_title_url_version(manga_title: str) -> str:
        '''
        Get rid of non-word characters, each whitespace sequence replace with an underscore.
        '''

        # get rid of non-word characters
        only_word_characters = re.sub('[^\\w]', ' ', manga_title)

        only_word_characters = only_word_characters.strip()

        # join all words with underscores
        no_whitespaces = re.sub('\\s+', '_', only_word_characters)

        return f'{no_whitespaces.lower()}'

    @staticmethod
    def get_chapter_download_link(manga_title_url_version: str, chapter_number: str) -> str:
        return f'https://images.mangafreak.net/downloads/{manga_title_url_version}_{chapter_number}'

    @staticmethod
    def add_leading_zeroes(chapter_name: str, length: int = 4) -> str:
        '''
        Examples, when length is 4:

        '43' -> '0043'

        '43e' -> '0043e'
        '''

        match = re.search('^\\d+(.*)', chapter_name)

        if match is None:
            return chapter_name

        nondigit_part = match.group(1)

        return chapter_name.rjust(length + len(nondigit_part), '0')

    @classmethod
    def download_chapter(cls, manga_title_url_version: str, chapter_number: str) -> str:
        '''
        Download chapter (zip-archive with JPG-images) and get output file path.
        '''

        # generate download link
        link = cls.get_chapter_download_link(manga_title_url_version, chapter_number)

        # create required directories
        base_path = os.path.join(os.getcwd(), cls.DOWNLOADS_DIRECTORY, manga_title_url_version)
        os.makedirs(base_path, exist_ok=True)

        # generate output file path
        output_file_path = os.path.join(base_path, f'{cls.add_leading_zeroes(chapter_number)}.zip')

        # skip download if file already exists
        if os.path.exists(output_file_path):
            print(f'Chapter is already downloaded at {output_file_path}')

            return output_file_path

        # open file for writing and make HTTP-request
        with open(output_file_path, 'wb') as output_file, requests.get(link, stream=True) as response:

            print(f'Downloading from {link}:')

            if response.status_code != requests.status_codes.codes['ok']:
                raise ConnectionError(f'Server responded with status code {response.status_code}')

            # hide cursor
            print('\033[?25l', end='')

            chunk_number = 1

            for chunk in response.iter_content(chunk_size=cls.DOWNLOAD_CHUNK_SIZE_BYTES):

                output_file.write(chunk)

                print(f'\rDownloaded: {os.path.getsize(output_file_path)} bytes', end='')

                chunk_number += 1

            # show cursor
            print('\033[?25h')

            print(f'Chapter {chapter_number} saved to {output_file_path}')

        return output_file_path

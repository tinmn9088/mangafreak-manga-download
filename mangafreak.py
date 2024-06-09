from bs4 import BeautifulSoup
import re


class MangafreakService:

    TITLE_SELECTOR = '.manga_series_data h1'

    CHAPTER_LIST_SELECTOR = '.manga_series_list_section tbody'

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
        only_word_characters = re.sub('[^\w]', ' ', manga_title)

        only_word_characters = only_word_characters.strip()

        # join all words with underscores
        no_whitespaces = re.sub('\s+', '_', only_word_characters)

        return f'{no_whitespaces.lower()}'

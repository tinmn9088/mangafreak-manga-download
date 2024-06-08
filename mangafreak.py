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
    def get_image_links(title: str, chapter_number: str) -> list[str]:
        pass

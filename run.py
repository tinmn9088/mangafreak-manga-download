import os
from cli import ArgumentService
from mangafreak import MangafreakService


settings = ArgumentService.get_settings()

print('Running with settings:', vars(settings))

# parse HTML
title, chapter_numbers = MangafreakService.parse_html(settings.chapter_list_html_path)

# transform title to its url version
title_url_version = MangafreakService.get_title_url_version(title)

# download chapters (zip-archives)
downloaded_file_paths = []

for chapter_number in chapter_numbers:

    downloaded_file_path = MangafreakService.download_chapter(title_url_version, chapter_number)

    downloaded_file_paths.append(downloaded_file_path)

print(f'Files downloaded: {len(downloaded_file_paths)}')

downloads_path = os.path.commonpath(downloaded_file_paths)

print(sorted(os.listdir(downloads_path)))

# TODO: assemble images in PDF

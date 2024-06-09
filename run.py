import os
import zipfile
from pathlib import Path
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

# prepare extraction directory
extraction_common_path = os.path.join(downloads_path, 'extracted')
os.makedirs(extraction_common_path, exist_ok=True)

# iterate through downloaded archives and extract images
archive_number = 0

for archive_name in sorted(os.listdir(downloads_path)):

    # get archive full path
    archive_path = os.path.join(downloads_path, archive_name)

    print(f'Extracting {archive_path}:')

    # prepare extraction directory for this specific archive
    extraction_path = os.path.join(
        extraction_common_path,
        f'{(archive_number // settings.chapters_per_file + 1):03d}',  # group archives
        Path(archive_name).stem
    )

    os.makedirs(extraction_path, exist_ok=True)

    # extract archive
    with zipfile.ZipFile(archive_path, 'r') as archive_file:
        archive_file.extractall(extraction_path)

    archive_number += 1

# TODO: assemble images in PDF

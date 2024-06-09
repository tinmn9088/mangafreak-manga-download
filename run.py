import os
import re
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
EXTRACTION_COMMON_DIRECTORY = 'extracted'
extraction_common_path = os.path.join(downloads_path, EXTRACTION_COMMON_DIRECTORY)
os.makedirs(extraction_common_path, exist_ok=True)

# iterate through downloaded archives and extract images
archive_number = 0
extraction_paths = []

for archive_name in sorted(filter(lambda p: p != EXTRACTION_COMMON_DIRECTORY, os.listdir(downloads_path))):

    # get archive full path
    archive_path = os.path.join(downloads_path, archive_name)

    print(f'Extracting {archive_path} ... ', end='')

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

    extraction_paths.append(extraction_path)

    archive_number += 1

    print('Done')

# rename images in natural order manner
for extraction_path in extraction_paths:

    print(f'Renaming images in {extraction_path} ... ', end='')

    for image_name in os.listdir(extraction_path):

        # extract image number
        match = re.search('(\\d+)(\\..*)$', image_name)

        if match is None:
            raise ValueError(f'Cannot extract image number from {image_name}')

        image_number = int(match.group(1))
        remaining_part = match.group(2)

        image_path = os.path.join(extraction_path, image_name)

        # prepare image new path
        image_new_directory, chapter_number = os.path.split(extraction_path)

        image_new_name = f'{chapter_number}_{image_number:03d}{remaining_part}'

        image_new_path = os.path.join(image_new_directory, image_new_name)

        # rename and move image
        os.renames(image_path, image_new_path)

    print('Done')

# TODO: assemble images in PDF

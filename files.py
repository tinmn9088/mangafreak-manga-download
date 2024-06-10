import os
import re
from zipfile import ZipFile
from pathlib import Path
from settings import Settings


class FileService:

    EXTRACTION_COMMON_DIRECTORY = 'extracted'

    @classmethod
    def extract_archives(cls, downloads_path: str, settings: Settings) -> list[str]:
        '''
        Extract all zip-archives from downloads_path and return the list of
        destination directories.
        '''

        # prepare extraction directory
        extraction_common_path = os.path.join(downloads_path, cls.EXTRACTION_COMMON_DIRECTORY)
        os.makedirs(extraction_common_path, exist_ok=True)

        # iterate through downloaded archives and extract images
        archive_number = 0
        extraction_paths = []

        for archive_name in sorted(filter(lambda p: p.endswith('.zip'), os.listdir(downloads_path))):

            # get archive full path
            archive_path = os.path.join(downloads_path, archive_name)

            print(f'Extracting {archive_path} ... ', end='')

            # prepare extraction directory for this specific archive
            extraction_path = os.path.join(
                extraction_common_path,

                f'{(archive_number // settings.chapters_per_file + 1):04d}',  # group archives
                Path(archive_name).stem
            )

            os.makedirs(extraction_path, exist_ok=True)

            # extract archive
            with ZipFile(archive_path, 'r') as archive_file:
                archive_file.extractall(extraction_path)

            extraction_paths.append(extraction_path)

            archive_number += 1

            print('Done')

        return extraction_paths

    @staticmethod
    def prepare_images(extraction_paths: list[str]) -> set[str]:
        '''
        Rename images from extraction_paths in natural order manner and return
        their new common paths.
        '''

        image_directory_paths = set()

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

                image_directory_paths.add(image_new_directory)

            print('Done')

        return sorted(list(image_directory_paths))

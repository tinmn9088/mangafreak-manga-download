import os
import subprocess
from settings import Settings
from cli import MessageService


class ImageMagickService:

    PDF_COMMON_DIRECTORY = 'pdf'

    @classmethod
    def convert_images_to_pdf(
        cls,
        downloads_path: str,
        manga_title_url_version: str,
        image_directory_paths: list[str],
        settings: Settings
    ) -> list[str]:
        '''
        Assemble images from image_directory_paths in PDFs and return their paths.
        '''

        # create required directories
        base_path = os.path.join(os.getcwd(), downloads_path, cls.PDF_COMMON_DIRECTORY)
        os.makedirs(base_path, exist_ok=True)

        pdf_number = 1
        pdf_paths = []

        # iterate through directories with images
        for image_directory_path in image_directory_paths:

            # prepare PDF name
            pdf_name = ''

            if settings.author is not None:
                pdf_name += settings.author + '. '

            if settings.title is not None:
                pdf_name += settings.title
            else:
                pdf_name += manga_title_url_version

            pdf_name += f'. - {pdf_number:02d}.pdf'

            # prepare PDF path
            pdf_path = os.path.join(base_path, pdf_name)

            # prepare command to run ImageMagick
            args = ['convert', f'{image_directory_path}/*', pdf_path]

            if settings.verbose:
                args.insert(1, '-monitor')

            if settings.verbose:
                print(f'Converting images from {image_directory_path}:')

            else:

                # need to flush, otherwise it is likely not to print before converting is finished
                print(f'Converting images from {image_directory_path} ... ', end='', flush=True)

            # run ImageMagick
            try:
                subprocess.check_output(args)

                if not settings.verbose:
                    print('Done')

            except subprocess.CalledProcessError as e:
                print(f'\n\n{MessageService.WARN_PREFIX} Non-zero exit code (check {pdf_path}): {e.output}', end='\n\n')

            pdf_number += 1

            pdf_paths.append(pdf_path)

        return pdf_paths

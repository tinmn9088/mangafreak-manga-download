from cli import ArgumentService

settings = ArgumentService.get_settings()

print('Running with settings:', vars(settings))

print('Not implemented')

# TODO: generate url of the manga page, retrieve HTML and parse the list of chapters

# TODO: generate urls of images and download them

# TODO: assemble images in PDF

# -*- coding: utf-8 -*-
"""
Commandline interface
"""

import click

from imagefactory import create_image


# TODO: confirm for overwriting file is exists
# TODO: Verbosity


@click.command()
@click.version_option()
@click.option('--name', '-n', default='untitled',
              help='Name of the file. If name is written with extension it'
                   'overwrites any filetype that is supplied.')
@click.option('--width', '-w', default=48,
              help='Width of the image')
@click.option('--height', '-h', default=48,
              help='Height of the image.')
@click.option('--filetype', '-ft', default='png',
              help='Filetype of the image. For example "png" or "svg"')
@click.option('--text', '-t', default=None,
              help='Text that is written in the image.')
@click.option('--savedir', '-d', default='',
              help='Directory where image should be saved.')
@click.option('--overwrite', is_flag=True,
              help='If image exists in the file system overwrites it.')
def main(name, width, height, filetype, text, savedir, overwrite):
    """Console script for imagefactory"""
    create_image(name, filetype, width, height, text, savedir, overwrite)


if __name__ == "__main__":
    main()

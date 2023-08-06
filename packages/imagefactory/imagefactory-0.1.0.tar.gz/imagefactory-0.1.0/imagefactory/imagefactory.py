import logging
import os
import shutil
from io import BytesIO, StringIO, TextIOBase

from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)


# FIXME: Text size
# TODO: Caching?
# TODO: Image size choises: Icon, ...
# TODO: Width and height units (cm, mm, em, px, pt, pc, in, ...) default: px
# TODO: Background color


def _create_bitmap(name, width, height, filetype, text):
    """
    Create bitmap image.

    Returns:
        BytesIO:
    """
    file = BytesIO()
    file.name = name + '.' + filetype
    image = Image.new('RGBA', size=(width, height), color=(128, 128, 128))
    draw = ImageDraw.Draw(image)
    size = draw.textsize(text)
    draw.text(((width - size[0]) / 2, (height - size[1]) / 2), text)
    image.save(file, format=filetype)
    file.seek(0)
    return file


def _create_svg(name, width, height, text):
    """
    Create svg image.

    Returns:
        StringIO:
    """
    import svgwrite
    file = StringIO()
    file.name = name + '.svg'
    center = (width / 2, height / 2)
    image = svgwrite.Drawing(file.name, profile='tiny', height=height,
                             width=width)
    image.add(image.rect(insert=(0, 0), size=(width, height), fill='gray'))
    # TODO: Test if text fits inside rectangle
    # image.add(image.text(text, insert=center))
    image.write(file)
    file.seek(0)
    return file


def _save_image(image, filedir, overwrite):
    """
    Save in memory image to a file.

    Args:
        image (io.IOBase):
            In memory image.

        filedir (str):
            Path to the directory where `image` should be saved

    Raises:
        TypeError: If `image` is not correct type.
        FileExistsError: If file with name `image.name` exists in `filedir`.
    """
    if isinstance(image, TextIOBase):
        # Write as text file
        mode = 'wt'
    else:
        # Write as binary file
        mode = 'wb'

    filepath = os.path.join(filedir, image.name)
    if os.path.exists(filepath) and not overwrite:
        raise FileExistsError(
            'File with name "{name}" already exists in path "{filepath}".'
            ''.format(name=image.name, filepath=filepath)
        )
    with open(filepath, mode) as file:
        shutil.copyfileobj(image, file)


def create_image(name='untitled', filetype='png', width=48, height=48,
                 text=None, savedir=None, overwrite=False):
    """
    Creates in memory images for testing [#]_. Bitmap images are created

    >>> from imagefactory import create_image
    >>> create_image()
    <_io.BytesIO object at ...>

    Vector graphic images can be created

    >>> from imagefactory import create_image
    >>> create_image(filetype='svg')
    <_io.StringIO object at ...>

    Args:
        name (str):
            - ``name`` Name of the file.
            - ``name.ext`` If extension is supplied it overwrites any supplied
              filetype.

        width (int):
            Positive integer

        height (int):
            Positive integer

        filetype (str):
            Filetype is extension string: ``jpeg, png, gif, svg``

        text (str, optional):
            - Default:  ``None`` uses ``{width}x{height}``
            - Otherwise supplied ``text`` string is used.

        savedir (str, optional):
            - Default: ``None`` doesn't save the image
            - Otherwise save image to ``savedir`` directory

        overwrite (Boolean):
            Boolean flag for toggling if existing file in the same filepath
            should be overwritten.

    Returns:
        BytesIO|StringIO:
            Image as ``BytesIO`` or ``StringIO`` object. It can be used in same fashion
            as file object created by opening a file.

    References:

        .. [#] http://wildfish.com/blog/2014/02/27/generating-in-memory-image-for-tests-python/
    """
    logging.info("")
    name, ext = os.path.splitext(name)
    if ext:
        filetype = ext

    if text is None:
        text = "{width}x{height}".format(width=width, height=height)

    if filetype == 'svg':
        try:
            image = _create_svg(name, width, height, text)
        except ImportError as error:
            raise Exception(
                'You need to install svgwrite to create vector graphics.'
                '{msg}'.format(msg=error)
            )
    else:
        image = _create_bitmap(name, width, height, filetype, text)

    if savedir is not None:
        _save_image(image, savedir, overwrite)

    return image

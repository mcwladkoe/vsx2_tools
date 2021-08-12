import os
from io import BytesIO
import platform
from typing import Tuple, Optional

from PIL import Image, ImageDraw, ImageFont, ImageColor
from flask import Blueprint, render_template, request, abort, Request, send_file
from flask_babel import _, get_locale
from pyclamd import ClamdUnixSocket, ConnectionError as ClamdConnectionError

meme_generator = Blueprint('meme_generator', __name__, url_prefix='/meme_generator')


class MemeGeneratorValidationError(Exception):
    def __init__(self, *args, status_code=400):
        super().__init__(*args)
        self.status_code = status_code


class MemeGenerator:
    def __init__(self, file, text: str, text_color: str):
        self.__image: Image = Image.open(file)

        self.__image_width, self.__image_height = self.__image.size

        self.__text: str = text
        self.__draw: ImageDraw.Draw = ImageDraw.Draw(self.__image)

        self.__max_font_size_cached: Optional[int] = None
        self.__load_font()
        self.__load_text_size()
        self.__text_color = ImageColor.getcolor(text_color, 'RGB')

    def __load_font(self):
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        path_to_font = os.path.join(current_file_path, "..", "static", "fonts", "Lobster-Regular.ttf")
        self.__font: ImageFont = ImageFont.truetype(path_to_font, self.__font_size)

    def __load_text_size(self):
        self.__text_width, self.__text_height = self.__draw.textsize(self.__text, self.__font)

    @property
    def __font_size(self) -> int:
        calculated_size = int(self.__image_width / len(self.__text))
        if calculated_size > self.__max_font_size:
            return self.__max_font_size
        return calculated_size

    @property
    def __max_font_size(self) -> int:
        if self.__max_font_size_cached:
            return self.__max_font_size_cached

        size = int(self.__image_height / 10)
        if size < 5:
            raise MemeGeneratorValidationError('invalid image size:( we cannot use this image as template')

        self.__max_font_size_cached = size

        return size

    @property
    def __text_position(self) -> Tuple[int, int]:
        x = int((self.__image_width - self.__text_width + 1) / 2)
        y = int(self.__image_height - self.__font_size * 1.5)
        return x, y

    def __call__(self) -> Tuple[BytesIO, str, str]:
        self.__draw.text(self.__text_position, self.__text, self.__text_color, font=self.__font)

        img_io: BytesIO = BytesIO()
        self.__image.save(img_io, self.__image.format, quality=100)
        img_io.seek(0)

        return img_io, self.__image.get_format_mimetype(), self.__image.format.lower()


def meme_generator_request_processor(flask_request: Request) -> Tuple[BytesIO, str, str]:
    if 'image' not in flask_request.files:
        raise MemeGeneratorValidationError('Please select image')
    text = flask_request.values.get('text')
    if not text:
        raise MemeGeneratorValidationError('Please input text')
    text_color = flask_request.values.get('text_color') or '#ffffff'

    f = flask_request.files['image']

    if platform.system() == 'Linux':
        socket = ClamdUnixSocket()
        try:
            result = socket.scan_stream(f)
        except ClamdConnectionError:
            raise MemeGeneratorValidationError('Something went wrong :( Please contact me at me@vldsx.com',
                                               status_code=500)
        finally:
            socket._close_socket()
        if result:
            raise MemeGeneratorValidationError('Virus detected in file :(')
    return MemeGenerator(f, text, text_color)()


@meme_generator.route('/', methods=["get", "post"])
def index():
    if request.values.get('secret') != 'hb.png112233':
        return abort(404)
    error = None
    if request.method == 'POST':
        try:
            file, mimetype, file_type = meme_generator_request_processor(request)
            kwargs = {
                'mimetype': mimetype
            }
            if request.values.get('download') == 'Download':
                kwargs.update({
                    'as_attachment': True,
                    'download_name': f'meme_from_vldsx.{file_type}',
                })
            return send_file(file, **kwargs)
        except MemeGeneratorValidationError as e:
            error = e

    return render_template(
        "meme_generator.html",
        page_title=_('memeGeneratorPageTitle'),
        locale=get_locale(),
        error_message=str(error) if error else '',
        meme_text=request.values.get('text') or '',
        text_color=request.values.get('text_color') or '#ffffff'
    ), error.status_code if error and error.status_code else 200

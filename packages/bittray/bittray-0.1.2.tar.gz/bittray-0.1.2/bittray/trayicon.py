import cStringIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops
from matplotlib import font_manager


# TODO configurable
WIDTH = 400
HEIGHT = 400


# TODO this should probaly extend wx.TaskBarIcon
class TrayIcon(object):
    """
    This object draw an image with a text inside it.
    """
    def __init__(self, conf):
        self.conf = conf
        self.font = ImageFont.truetype(
            self.conf.get_font_path(),
            self.conf.get_int('Look', 'size'),
        )

    def trim(self, im):
        """
        Auto-trim
        """
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    def get_image(self, text):
        """
        Return a file like object containing the image with text.
        """
        img = Image.new('RGB', (WIDTH, HEIGHT), self.conf.get_color('Look', 'background'))
        d = ImageDraw.Draw(img)
        d.text(
            self.conf.get_color('Look', 'background'),
            text,
            font=self.font,
            fill=self.conf.get_color('Look', 'color')
        )
        img = self.trim(img)
        buf = cStringIO.StringIO()
        img.save(buf, 'png')
        buf.seek(0)
        return buf

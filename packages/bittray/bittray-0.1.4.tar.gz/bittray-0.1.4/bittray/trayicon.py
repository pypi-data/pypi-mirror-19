try:
    import cStringIO as io
except ImportError:
    import io

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageChops
from matplotlib import font_manager
import wx


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

    def get_icon(self, text):
        """
        Return a wx icon from a file like object containing the image
        with text.

        TODO: transparency support
        """
        background = self.conf.get_color('Look', 'background')
        foreground = self.conf.get_color('Look', 'color')
        font = ImageFont.truetype(
            self.conf.get_font_path(),
            self.conf.get_int('Look', 'size'),
        )
        mask = Image.new('RGB', (WIDTH, HEIGHT), background)
        draw = ImageDraw.Draw(mask)
        draw.text(
            background,
            text,
            font=font,
            fill=foreground,
        )
        mask = self.trim(mask)
        buf = io.StringIO()
        mask.save(buf, 'png')
        buf.seek(0)
        icon = wx.IconFromBitmap(
            wx.BitmapFromImage(
                wx.ImageFromStream(
                    buf,
                    wx.BITMAP_TYPE_PNG
                )
            )
        )
        return icon

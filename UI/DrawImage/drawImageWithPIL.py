from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui
import omni.kit.app
import carb.events
import asyncio
import math
import itertools

# PIL exists in "kit/extscore/omni.kit.pip_archive/pip_prebundle".
from PIL import Image, ImageDraw, ImageFont

# Get main window viewport.
window = omni.ui.Window('Viewport')

# ref : omni.kit.window.images  extension.py

# ------------------------------------------.
# Managing overlay image.
# ------------------------------------------.
class OverlayImageBuffer:
    _width = 256
    _height = 256    
    _byte_provider = None
    _byte_data = None

    def __init__(self):
        self._width = 256
        self._height = 256    
        self._byte_provider = None
        self._byte_data = None

    def startup (self, width : int, height : int):
        self._byte_provider = omni.ui.ByteImageProvider()
        self._width  = width
        self._height = height

        # default format omni.ui.TextureFormat.RGBA8_UNORM.
        self._byte_data = [0] * (4 * self._width * self._height)

        self._byte_provider.set_bytes_data(self._byte_data, [self._width, self._height])

    def update (self):
        self._byte_provider.set_bytes_data(self._byte_data, [self._width, self._height])

# ------------------------------------------.
# Draw image with PIL.
# ------------------------------------------.
class DrawImageWithPIL:
    _timeCount = 0
    _image = None
    _draw  = None
    _overlayImageBuffer = None

    def __init__(self):
        self._image = None
        self._draw  = None
        self._overlayImageBuffer = None

    def __del__(self):
        self._image = None
        self._draw  = None

    def getWidth (self):
        return self._overlayImageBuffer._width

    def getHeight (self):
        return self._overlayImageBuffer._height

    def getByteProvider (self):
        return self._overlayImageBuffer._byte_provider

    def startup (self, width : int, height : int):
        # Create new image.
        self._image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self._draw  = ImageDraw.Draw(self._image)

        self._overlayImageBuffer = OverlayImageBuffer()
        self._overlayImageBuffer.startup(width, height)

    def draw (self):
        # Draw rectangle (fill).
        self._draw.rectangle((0, 0, self._image.width, self._image.height), fill=(0, 0, 0, 0))

        # Draw rectangle (fill).
        self._draw.rectangle((100, 100, 200, 200), fill=(255, 0, 0))

        # Draw rectangle.
        self._draw.rectangle((100, 220, 200, 320), outline=(0, 0, 255), width=1)

        # Draw line.
        self._draw.line((0, 0, self._image.width, self._image.height), fill=(0, 255, 0), width=2)

        # Draw circle.
        self._draw.ellipse((100, 400, 150, 450), outline=(0, 0, 255), width=2)

        # Draw circle (fill).
        self._draw.ellipse((280, 300, 380, 400), fill=(0, 0, 255))

    def update (self):
        self.draw()

        # Get image data(RGBA buffer).
        imgD = self._image.getdata()

        # Converting a 2d array to a 1d array.
        self._overlayImageBuffer._byte_data = list(itertools.chain.from_iterable(imgD))

        # Update omni.ui.ByteImageProvider.
        self._overlayImageBuffer.update()

# ------------------------------------------.
# Update event.
# ------------------------------------------.
_drawImageWithPIL = None
_img1 = None

def on_update(e: carb.events.IEvent):
    global _drawImageWithPIL
    global _img1

    if _drawImageWithPIL == None:
        _drawImageWithPIL = DrawImageWithPIL()
        _drawImageWithPIL.startup(512, 512)
        _drawImageWithPIL.update()

    with window.frame:
        with omni.ui.VStack(height=0):
            with omni.ui.Placer(offset_x=8, offset_y=8):
                _img1 = omni.ui.ImageWithProvider(_drawImageWithPIL.getByteProvider(), width=_drawImageWithPIL.getWidth(), height=_drawImageWithPIL.getHeight())

# ------------------------------------------.
# Register for update events.
# To clear the event, specify "subs=None".
subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update, name="Test update")



from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui
import omni.kit.app
import carb.events
import asyncio
import math

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
    _timeCount = 0

    def __init__(self):
        self._timeCount = 0
        self._width = 512
        self._height = 256    
        self._byte_provider = None
    
    def startup (self):
        self._byte_provider = omni.ui.ByteImageProvider()

    def update (self):
        # default format omni.ui.TextureFormat.RGBA8_UNORM.
        byte_data = [0] * (4 * self._width * self._height)

        for x in range(self._width):
            hV = 100.0
            v = math.cos((float)(x + self._timeCount) * 1.2 * math.pi / 180.0) * hV
            iV = 128 + (int)(v)

            iPos = (iV * self._width + x) * 4
            byte_data[iPos + 0] = 255       # Red
            byte_data[iPos + 1] = 255       # Green
            byte_data[iPos + 2] = 0         # Blue
            byte_data[iPos + 3] = 255       # Alpha

        self._byte_provider.set_bytes_data(byte_data, [self._width, self._height])

        self._timeCount += 1

# ------------------------------------------.
# Update event.
# ------------------------------------------.
_imgBuffer = None
_img1 = None

def on_update(e: carb.events.IEvent):
    global _imgBuffer
    global _img1

    if _imgBuffer == None:
        _imgBuffer = OverlayImageBuffer()
        _imgBuffer.startup()
        _imgBuffer.update()

    with window.frame:
        with omni.ui.VStack(height=0):
            with omni.ui.Placer(offset_x=8, offset_y=8):
                _img1 = omni.ui.ImageWithProvider(_imgBuffer._byte_provider, width=_imgBuffer._width, height=_imgBuffer._height)

    _imgBuffer.update()

# ------------------------------------------.
# Register for update events.
# To clear the event, specify "subs=None".
subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update, name="Test update")



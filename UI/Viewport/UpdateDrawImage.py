import omni.ui
import omni.kit.app
import carb.events
import carb.tokens
import asyncio
import time
import itertools
from pathlib import Path
import os.path

# PIL exists in "kit/extscore/omni.kit.pip_archive/pip_prebundle".
from PIL import Image, ImageDraw, ImageFont

# Get main window viewport.
window = omni.ui.Window('Viewport')

countV = 0
timeV = time.time()

# ------------------------------------------.
# Load image.
# ------------------------------------------.
class LoadImageRGBA:
    _byte_provider = None
    _width  = 0
    _height = 0

    def __init__(self):
        pass

    def Open (self, path : str):
        try:
            # Load image (RGBA).
            im = Image.open(path).convert('RGBA')

            # Get image size.
            self._width  = im.size[0]
            self._height = im.size[1]

            # Get image data(RGBA buffer).
            imgD = im.getdata()

            # Converting a 2d array to a 1d array.
            byte_data = list(itertools.chain.from_iterable(imgD))

            self._byte_provider = omni.ui.ByteImageProvider()
            self._byte_provider.set_bytes_data(byte_data, [self._width, self._height])

        except Exception as e:
            self._width  = 0
            self._height = 0
            self._byte_provider = None
            print(e)
            return False

        return True
    
    def GetWidth (self):
        return self._width

    def GetHeight (self):
        return self._height

    def GetByteProvider (self):
        return self._byte_provider

# Image data.
imgData = None

# ------------------------------------------.
# Update event.
# ------------------------------------------.
def on_update(e: carb.events.IEvent):
    global countV
    global timeV
    global imgData

    # Process every second.
    curTimeV = time.time()
    if curTimeV - timeV > 1:
        timeV = curTimeV
        countV += 1

    # Update UI.
    with window.frame:
        with omni.ui.ZStack():
            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=20, offset_y=50):
                    # Set label.
                    f = omni.ui.Label("counter = " + str(countV))
                    f.visible = True
                    f.set_style({"color": 0xff00ffff, "font_size": 32})

            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=220, offset_y=150):
                    # "omni.ui.Image" cannot be used with "get_update_event_stream().create_subscription_to_pop".
                    # Use "omni.ui.ImageWithProvider" instead.
                    byte_provider = imgData.GetByteProvider()
                    imgWidth  = imgData.GetWidth()
                    imgHeight = imgData.GetHeight()
                    omni.ui.ImageWithProvider(byte_provider, width=imgWidth, height=imgHeight)

# ------------------------------------------.

# Kit file path.
kitAbsPath = os.path.abspath(carb.tokens.get_tokens_interface().resolve("${kit}"))

# Load image (RGBA).
imagePath = Path(kitAbsPath).joinpath("resources").joinpath("desktop-icons")
imagePath = f"{imagePath}/omniverse_64.png"

imgData = LoadImageRGBA()
if imgData.Open(imagePath):
    # Register for update events.
    # To clear the event, specify "subs=None".
    subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update, name="Test update")



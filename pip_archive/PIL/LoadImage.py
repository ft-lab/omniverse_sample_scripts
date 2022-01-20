# PIL exists in "kit/extscore/omni.kit.pip_archive/pip_prebundle".
from PIL import Image

# Load image from file.
path = "K:/NVIDIA_omniverse/images/omniverse_64.png"
im = None
try:
    im = Image.open(path)

    # Get image size.
    wid = im.size[0]
    hei = im.size[1]
    print("Image size : " + str(wid) + " x " + str(hei))

    # Get format (PNG, JPEG, etc).
    print("Format : " + str(im.format))

    # Get mode (RGB, RGBA, etc.).
    print("Mode : " + str(im.mode))

except Exception as e:
    print(e)


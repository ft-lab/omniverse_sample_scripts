# PIL exists in "kit/extscore/omni.kit.pip_archive/pip_prebundle".
from PIL import Image, ImageDraw, ImageFont

# Create new image.
im = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

draw = ImageDraw.Draw(im)

# Draw rectangle (fill).
draw.rectangle((100, 100, 200, 200), fill=(255, 0, 0))

# Draw rectangle.
draw.rectangle((100, 220, 200, 320), outline=(0, 0, 255), width=1)

# Draw line.
draw.line((0, 0, im.width, im.height), fill=(0, 255, 0), width=2)

# Draw circle.
draw.ellipse((100, 400, 150, 450), outline=(0, 0, 255), width=2)

# Draw circle (fill).
draw.ellipse((280, 300, 380, 400), fill=(0, 0, 255))

# Polygon.
vers = ((40, 20), (140, 120), (180, 60))
draw.polygon(vers, outline=(128, 0, 0))

# Polygon (fill).
vers = ((240, 20), (340, 120), (380, 60))
draw.polygon(vers, fill=(128, 128, 0))

# Font.
font = None
try:
    # The ttf font path should be replaced according to your environment.
    basePath = "K:/fonts"
    fontPath = basePath + "/SourceHanSansJP-Bold.otf"
    font = ImageFont.truetype(fontPath, 48)
except Exception as e:
    print(e)    

# Draw text.
if font != None:
    draw.multiline_text((16, 40), 'Draw Text!', fill=(0, 128, 0))

# Save image.
# Rewrite it to any file path and uncomment the following.
#im.save("K:/NVIDIA_omniverse/images/out.png", quality=95)

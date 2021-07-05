import omni.ui
import random

# Get main window viewport.
window = omni.ui.Window('Viewport')

rectSize = 5.0

with window.frame:
    # Use ZStack for multiple displays.
    with omni.ui.ZStack():
        for i in range(50):
            px = random.random() * 500.0
            py = random.random() * 500.0
            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=px, offset_y=py):
                    # Set rectangle.
                    rect = omni.ui.Rectangle(width=rectSize, height=rectSize)

                    # Color : 0xAABBGGRR.
                    rect.set_style({"background_color":0xff0000ff})

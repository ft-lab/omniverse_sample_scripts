import omni.ui

# Get main window viewport.
window = omni.ui.Window('Viewport')

with window.frame:
    with omni.ui.VStack():
        # Display position from top left.
        with omni.ui.Placer(offset_x=20, offset_y=50):
            # Set label.
            f = omni.ui.Label("Hello Omniverse!", alignment=omni.ui.Alignment.LEFT_TOP)
            f.visible = True

            # Color : 0xAABBGGRR.
            f.set_style({"color": 0xff00ffff, "font_size": 32})


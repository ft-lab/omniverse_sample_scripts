import omni.ui as ui

# Get main window viewport.
window = omni.ui.Window('Viewport')

with window.frame:
    with ui.VStack():
        # Display position from top left.
        with ui.Placer(offset_x=20, offset_y=50):
            # Set label.
            f = ui.Label("Hello Omniverse!", alignment=ui.Alignment.LEFT_TOP)
            f.visible = True

            # Color : 0xAABBGGRR.
            f.set_style({"color": 0xff00ffff, "font_size": 32})


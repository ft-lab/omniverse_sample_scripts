import omni.ui as ui

# Get main window viewport.
window = omni.ui.Window('Viewport')

with window.frame:
    with ui.VStack(height=0):
        with ui.Placer(offset_x=20, offset_y=50):
            # Set label.
            f = ui.Label("Hello Omniverse!")
            f.visible = True
            f.set_style({"color": 0xff00ffff, "font_size": 32})

        with ui.Placer(offset_x=20, offset_y=0):
            f2 = ui.Label("Line2!")
            f2.visible = True
            f2.set_style({"color": 0xff00ff00, "font_size": 32})

        with ui.Placer(offset_x=20, offset_y=0):
            f3 = ui.Label("Line3!")
            f3.visible = True
            f3.set_style({"color": 0xff0000ff, "font_size": 32})

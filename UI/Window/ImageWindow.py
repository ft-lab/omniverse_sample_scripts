import omni.ui

# Create new window.
my_window = omni.ui.Window("New Window", width=300, height=200)

# ------------------------------------------.
with my_window.frame:
    with omni.ui.VStack(height=0):
        with omni.ui.Placer(offset_x=8, offset_y=8):
            f = omni.ui.Label("Hello Omniverse!")
            f.set_style({"color": 0xff00ffff, "font_size": 20})
        with omni.ui.Placer(offset_x=8, offset_y=0):
            # image search path :
            #    "kit_release/_build/windows-x86_64/release" or
            #    absolute path
            omni.ui.Image("resources/desktop-icons/omniverse_64.png", width=64, height=64, fill_policy=omni.ui.FillPolicy.PRESERVE_ASPECT_FIT, alignment=omni.ui.Alignment.LEFT_CENTER)


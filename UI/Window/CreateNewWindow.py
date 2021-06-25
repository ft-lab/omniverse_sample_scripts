import omni.ui

# Create new window.
my_window = omni.ui.Window("New Window", width=300, height=200)

# ------------------------------------------.
# Clicked button event.
# ------------------------------------------.
def onButtonClick(floatField):
    print("Button pushed.")

    # get/set FloatField.
    fCounter = floatField.model.get_value_as_float() 
    fCounter += 1.0
    floatField.model.set_value(fCounter)

# ------------------------------------------.
with my_window.frame:
    with omni.ui.VStack(height=0):
        floatField = None

        with omni.ui.Placer(offset_x=8, offset_y=8):
            # Set label.
            f = omni.ui.Label("Hello Omniverse!")
            f.set_style({"color": 0xff00ffff, "font_size": 20})

        with omni.ui.Placer(offset_x=8, offset_y=0):
            f2 = omni.ui.Label("Line2!")
            f2.set_style({"color": 0xff00ff00, "font_size": 20})

        with omni.ui.Placer(offset_x=8, offset_y=0):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Edit : ", width=50)
                floatField = omni.ui.FloatField(width=200, height=0)

        with omni.ui.Placer(offset_x=8, offset_y=0):
            # Set button.
            btn = omni.ui.Button("Push", width=200, height=0)
            btn.set_clicked_fn(lambda f = floatField: onButtonClick(f))

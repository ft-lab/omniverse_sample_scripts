import omni.ui

# Create new window.
my_window = omni.ui.Window("Input test window", width=300, height=200)

# ------------------------------------------.
with my_window.frame:
    sField = None
    sLabel = None

    # Reset StringField, Label.
    def onReset (uiField, uiLabel):
        if not uiField or not uiLabel:
            return

        uiField.model.set_value("")
        uiLabel.text = ""

    # Called when a value is changed in a StringField.
    def onValueChanged (uiFieldModel, uiLabel):
        if not uiFieldModel or not uiLabel:
            return

        v = uiFieldModel.get_value_as_string()
        uiLabel.text = v

    # Create window UI.
    with omni.ui.VStack(height=0):
        with omni.ui.Placer(offset_x=8, offset_y=8):
            with omni.ui.HStack(width=0):
                omni.ui.Label("Input  ")
                sField = omni.ui.StringField(width=120, height=14, style={"color": 0xffffffff})

        omni.ui.Spacer(height=4)
        sLabel = omni.ui.Label("text")
        omni.ui.Spacer(height=4)

        btn = omni.ui.Button(" Reset ") 

        # Specify the callback to be called when the Button is pressed.
        btn.set_clicked_fn(lambda f = sField, l = sLabel: onReset(f, l))

        # Specify a callback when a value is changed in a StringField.
        sField.model.add_value_changed_fn(lambda f, l = sLabel: onValueChanged(f, l))



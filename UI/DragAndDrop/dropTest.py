from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui

# Create new window.
my_window = omni.ui.Window("Drop test window", width=300, height=200)

# ------------------------------------------.
with my_window.frame:
    sField = None

    # Enable Drop.
    def drop_accept(url):
        return True

    # Called at Drop event.
    def drop (uiField, event):
        # prim path.
        vPath = event.mime_data

        # Get stage.
        stage = omni.usd.get_context().get_stage()

        # Get prim.
        if Sdf.Path(vPath):
            prim = stage.GetPrimAtPath(vPath)
            if prim.IsValid():
                # Set string.
                uiField.model.set_value(vPath)

    # Create window UI.
    with omni.ui.VStack(height=0):
        with omni.ui.Placer(offset_x=8, offset_y=8):
            omni.ui.Label("Please drop Prim below.")

        with omni.ui.Placer(offset_x=8, offset_y=0):
            omni.ui.Spacer(height=4)

        with omni.ui.Placer(offset_x=8, offset_y=0):
            sField = omni.ui.StringField(width=240, height=14, style={"color": 0xffffffff})
            sField.set_accept_drop_fn(drop_accept)
            sField.set_drop_fn(lambda a, w=sField: drop(w, a))


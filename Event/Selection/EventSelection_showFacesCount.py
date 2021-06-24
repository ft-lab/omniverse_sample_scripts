from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

import omni.ui
import omni.kit.app

# Get context.
context = omni.usd.get_context()

# Get stage.
stage = context.get_stage()

# Get main window viewport.
window = omni.ui.Window('Viewport')

# ---------------------------------------------.
# Get the number of faces in the mesh.
# ---------------------------------------------.
def GetFacesCount (prim):
    if prim.IsValid() == None:
        return 0
    typeName = prim.GetTypeName()

    allCou = 0
    if typeName == 'Mesh':
        m = UsdGeom.Mesh(prim)

        # If it is displayed.
        if m.ComputeVisibility() == 'inherited':
            # Get the number of faces of Mesh.
            allCou += len(m.GetFaceVertexCountsAttr().Get())

    # Recursively traverse the hierarchy.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        allCou += GetFacesCount(cPrim)

    return allCou

# ---------------------------------------------.
# Update Viewport UI.
# Show the number of faces of the selected shape in the Viewport.
# ---------------------------------------------.
def UpdateViewportUI(paths):
    if len(paths) == 0:
        with window.frame:
            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=20, offset_y=0):
                    omni.ui.Spacer(width=0, height=8)
        return

    with window.frame:
        with omni.ui.VStack(height=0):
            with omni.ui.Placer(offset_x=20, offset_y=50):
                f = omni.ui.Label("--- Selection Shapes ---")
                f.visible = True
                f.set_style({"color": 0xff00ffff, "font_size": 32})
            
            with omni.ui.Placer(offset_x=20, offset_y=0):
                omni.ui.Spacer(width=0, height=8)

            # Show selection shape name.
            for path in paths:
                prim = stage.GetPrimAtPath(path)
                if prim.IsValid() == True:
                    facesCou = GetFacesCount(prim)
                    with omni.ui.Placer(offset_x=28, offset_y=0):
                        f2 = omni.ui.Label('[ ' + prim.GetName() + ' ] faces ' + str(facesCou))
                        f2.visible = True
                        f2.set_style({"color": 0xff00ff00, "font_size": 32})

# ---------------------------------------------.
# Selected event.
# ---------------------------------------------.
def onStageEvent(evt):
    if evt.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
        # Get selection paths.
        selection = omni.usd.get_context().get_selection()
        paths = selection.get_selected_prim_paths()

        # Show selected shapes info.
        UpdateViewportUI(paths)

# ------------------------------------------------.
# Register for stage events.
# Specify "subs=None" to end the event.
subs = context.get_stage_event_stream().create_subscription_to_pop(onStageEvent, name="sampleStageEvent")

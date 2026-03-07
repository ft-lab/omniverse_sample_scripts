from pxr import Usd, UsdGeom
import omni.usd

def clear_display_color(prim: Usd.Prim):
    """
    Clear display color and opacity information of the specified prim.
    """
    geomPrim = UsdGeom.Gprim(prim)
    if not geomPrim:
        print(f"Prim at path {prim.GetPath()} is not a Gprim.")
        return

    # Clear displayColor attributes if they exist.    
    displayColorAttr = geomPrim.GetDisplayColorAttr()
    if displayColorAttr and displayColorAttr.IsDefined():
        displayColorAttr.Clear()

    # Clear displayOpacity attributes if they exist.
    displayOpacityAttr = geomPrim.GetDisplayOpacityAttr()
    if displayOpacityAttr and displayOpacityAttr.IsDefined():
        displayOpacityAttr.Clear()

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim:
        clear_display_color(prim)


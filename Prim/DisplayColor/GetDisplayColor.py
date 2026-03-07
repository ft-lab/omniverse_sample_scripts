from pxr import Usd, UsdGeom
import omni.usd

def get_display_color(prim: Usd.Prim):
    """
    Get display color information of the specified prim.
    """
    geomPrim = UsdGeom.Gprim(prim)
    if not geomPrim:
        print(f"Prim at path {prim.GetPath()} is not a Gprim.")
        return
    
    attr = geomPrim.GetDisplayColorAttr()
    if not attr:
        print(f"Prim at path {prim.GetPath()} does not have a displayColor attribute.")
        return

    # Get display color.
    colList = attr.Get()
    if not colList or len(colList) == 0:
        print(f"Prim at path {prim.GetPath()} has an empty displayColor attribute.")
        return

    if prim.IsA(UsdGeom.Mesh):
        primvar: UsdGeom.Primvar = geomPrim.GetDisplayColorPrimvar()

        # Get interpolation.
        #   constant: one value for the entire prim.
        #   uniform: one value for each face.
        #   vertex: one value for each vertex.
        interpolation = primvar.GetInterpolation()
        print(f"interpolation: {interpolation}")

        if interpolation == UsdGeom.Tokens.constant:
            print(f"Prim at path {prim.GetPath()} has a single displayColor: {colList[0]}")
        else:
            print(f"Prim at path {prim.GetPath()} has {len(colList)} displayColors.")

    else:
        print(f"Prim at path {prim.GetPath()} has a single displayColor: {colList[0]}")
    

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim:
        get_display_color(prim)



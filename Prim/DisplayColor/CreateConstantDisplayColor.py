from pxr import Gf, Usd, UsdGeom
import omni.usd

def create_constant_display_color(prim: Usd.Prim, color: Gf.Vec3f):
    """
    Create a constant display color for the specified prim.
    """
    geomPrim = UsdGeom.Gprim(prim)
    if not geomPrim:
        print(f"Prim at path {prim.GetPath()} is not a Gprim.")
        return

    # Specify a single displayColor.
    geomPrim.CreateDisplayColorPrimvar(UsdGeom.Tokens.constant)

    # Set displayColor value.
    geomPrim.CreateDisplayColorAttr([color])


# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim:
        create_constant_display_color(prim, Gf.Vec3f(0, 1, 0))


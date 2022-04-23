from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue

    # Get parent prim.
    parentPrim = prim.GetParent()
    if parentPrim.IsValid():
        print("[ " + prim.GetPath().pathString + " ]")
        print("  Parent : " + parentPrim.GetPath().pathString)

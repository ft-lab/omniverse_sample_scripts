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

    # Get children.
    pChildren = prim.GetChildren()
    if len(pChildren) >= 1:
        print("[ " + prim.GetPath().pathString + " ]")
        for cPrim in pChildren:
            print("   " + cPrim.GetPath().pathString)
   

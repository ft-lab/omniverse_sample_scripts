from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print(f"[ {prim.GetName()} ]")

        # Order of Transform elements.
        transformOrder = prim.GetAttribute('xformOpOrder').Get()
        for sV in transformOrder:
            print(f"  {sV}")



from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.GetTypeName() != "Mesh": 
        continue

    # USD 22.11 : The specification has been changed to use UsdGeom.PrimvarsAPI.
    primvarsAPI = UsdGeom.PrimvarsAPI(prim)

    primvars = 	primvarsAPI.GetPrimvars()
    if len(primvars) > 0:
        print("[" + prim.GetPath().pathString + "]")
        for primvar in primvars:
            primName = primvar.GetPrimvarName()
            typeName = primvar.GetTypeName()
            val      = primvar.Get()

            print("  " + primName + " (" + str(typeName) + ") : " + str(val))


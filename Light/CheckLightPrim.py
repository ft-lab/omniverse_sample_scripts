from pxr import Usd, UsdGeom, UsdPhysics, UsdLux, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# Check if prim is Light.
def checkLight (prim : Usd.Prim):
    typeName = prim.GetTypeName()

    if typeName == "DistantLight" or typeName == "CylinderLight" or \
    typeName == "DiskLight" or typeName == "DomeLight" or \
    typeName == "RectLight" or typeName == "SphereLight":
        return True
    
    return False

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)

    if checkLight(prim):
        print(f"[ {prim.GetPath().pathString} ] : {prim.GetTypeName()}")


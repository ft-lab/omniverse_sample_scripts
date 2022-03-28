from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

defaultPrim = stage.GetDefaultPrim()
if defaultPrim.IsValid():
    prims = []
    for prim in Usd.PrimRange(defaultPrim):
        if prim.IsA(UsdGeom.Mesh):      # For Mesh.
            prims.append(prim)

    for prim in prims:
        print(prim.GetName() + " (" + prim.GetPath().pathString + ")")


from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get prim.
orgPath = "/World/defaultLight"
prim = stage.GetPrimAtPath(orgPath)

if prim.IsValid():
    # Get Prim name.
    name = prim.GetName()
    print("Name : " + str(name))

    # Get Prim path.
    path = prim.GetPath()
    print("Path : " + str(path))

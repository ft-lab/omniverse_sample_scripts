from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

path = "/World"

# Get prim.
prim = stage.GetPrimAtPath(path)

# Use IsValid to check if the specified Prim exists.
print(path + " : " + str(prim.IsValid()))

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Default prim path.
defaultPrimPath = defaultPrim.GetPath().pathString

print("DefaultPrim : " + defaultPrimPath)
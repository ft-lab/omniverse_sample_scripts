from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

defaultPrimPath = defaultPrim.GetPath().pathString
path = defaultPrimPath + '/xform'

# Create empty node(Xform).
UsdGeom.Xform.Define(stage, path)


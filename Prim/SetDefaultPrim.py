from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create empty node(Xform).
path = "/NewWorld"
UsdGeom.Xform.Define(stage, path)
prim = stage.GetPrimAtPath(path)

# Set default prim.
stage.SetDefaultPrim(prim)


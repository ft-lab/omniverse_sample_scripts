from pxr import UsdGeom
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create empty node(Xform).
path = "/NewWorld"
UsdGeom.Xform.Define(stage, path)
prim = stage.GetPrimAtPath(path)

# Set default prim.
stage.SetDefaultPrim(prim)


from pxr import UsdGeom
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

defaultPrimPath = defaultPrim.GetPath().pathString
path = f"{defaultPrimPath}/xform"

# Create empty node(Xform).
UsdGeom.Xform.Define(stage, path)


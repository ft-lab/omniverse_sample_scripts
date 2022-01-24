from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString

# Create empty node(Xform).
path = defaultPrimPath + '/refShape'
UsdGeom.Xform.Define(stage, path)
prim = stage.GetPrimAtPath(path)

# Remove references.
prim.GetReferences().ClearReferences()

# Add a reference.
usdPath = "./sphere.usda"
prim.GetReferences().AddReference(usdPath)

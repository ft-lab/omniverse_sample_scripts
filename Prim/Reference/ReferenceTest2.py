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
#usdPath = "./cyawan/cyawan.usdc"
usdPath = "https://ft-lab.github.io/usd/omniverse/usd/cyawan/cyawan.usdc"
prim.GetReferences().AddReference(usdPath)

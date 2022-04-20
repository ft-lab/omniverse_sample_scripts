from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get root layer.
rootLayer = stage.GetRootLayer()

# Get real path.
realPath = rootLayer.realPath

print("realPath : " + realPath)

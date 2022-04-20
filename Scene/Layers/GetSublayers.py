from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get root layer.
rootLayer = stage.GetRootLayer()

# Get subLayer paths.
sublayerPaths = rootLayer.subLayerPaths

for path in sublayerPaths:
    print("  " + path)

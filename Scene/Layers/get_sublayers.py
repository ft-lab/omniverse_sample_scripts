import omni.usd
from pxr import Usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get root layer.
rootLayer = stage.GetRootLayer()

# Get subLayer paths.
sublayerPaths = rootLayer.subLayerPaths

for path in sublayerPaths:
    print(f"  {path}")

import omni.usd
from pxr import Sdf

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()

# Create anon layer and set it as edit target, then revert to previous
prev = stage.GetEditTarget().GetLayer()
anon = Sdf.Layer.CreateAnonymous()
paths = list(rootLayer.subLayerPaths)
paths.append(anon.identifier)
rootLayer.subLayerPaths = paths
print("Appended anonymous sublayer:", anon.identifier)

try:
    stage.SetEditTarget(anon)
    print("Switched edit target to:", anon.identifier)
finally:
    # restore previous
    stage.SetEditTarget(prev)
    print("Restored edit target to:", prev.identifier)

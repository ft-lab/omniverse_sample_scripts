import omni.usd

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()

print("Existing sublayers before removal:")
for p in rootLayer.subLayerPaths:
    print(" -", p)

# Try to remove last sublayer (if any)
paths = list(rootLayer.subLayerPaths)
if paths:
    removed = paths.pop()
    rootLayer.subLayerPaths = paths
    print("Removed sublayer:", removed)
else:
    print("No sublayers to remove")

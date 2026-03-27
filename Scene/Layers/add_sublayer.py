from pxr import Sdf
import omni.usd

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()
print("Root layer:", rootLayer.identifier)

# Create anonymous layer and append
# Note: Sdf.Layer.CreateAnonymous() creates an in-memory (anonymous)
# layer that exists only in memory for the session. It does not create
# a persistent USD file on disk unless you explicitly save or write it
# to a file (e.g., with Sdf.Layer.CreateNew or layer.Export()).
anon = Sdf.Layer.CreateAnonymous()
paths = list(rootLayer.subLayerPaths)
paths.append(anon.identifier)
rootLayer.subLayerPaths = paths
print("Appended anonymous sublayer:", anon.identifier)

# Remove it to avoid persistent change
paths = list(rootLayer.subLayerPaths)
if anon.identifier in paths:
    paths.remove(anon.identifier)
    rootLayer.subLayerPaths = paths
    print("Removed anonymous sublayer (cleanup)")
else:
    print("Anonymous sublayer not found for cleanup")

from pxr import Sdf
import omni.usd
import tempfile
import os

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()

print("Root layer:", rootLayer.identifier)

# List existing sublayers
print("Existing sublayers:")
for p in rootLayer.subLayerPaths:
    print(" -", p)

# Create an anonymous layer and add as a sublayer
anon = Sdf.Layer.CreateAnonymous()
print("Created anonymous layer:", anon.identifier)

# Add to root sublayers (append at end)
paths = list(rootLayer.subLayerPaths)
paths.append(anon.identifier)
rootLayer.subLayerPaths = paths
print("After adding anonymous sublayer:")
for p in rootLayer.subLayerPaths:
    print(" -", p)

# Switch editing layer to the new anonymous layer using the Usd.Stage API
try:
    stage.SetEditTarget(anon)
    edit_layer = stage.GetEditTarget().GetLayer()
    print("Current editing layer set to:", edit_layer.identifier)
except Exception as e:
    print("Could not set edit target via stage.SetEditTarget:", e)

# Write a small prim in the anonymous layer to demonstrate edit
try:
    anon.SetComment("Created by layer_create_edit_revert.py")
    anon.Save()
    print("Saved anonymous layer (may be stored as session layer):", anon.identifier)
except Exception as e:
    print("Could not save anonymous layer:", e)

# Revert: remove the anon sublayer we added
# Note: Since the anonymous layer is in-memory,
#  it won't persist across sessions and doesn't have a file path.
#  Removing it from the root layer's subLayerPaths effectively reverts the change.
paths = list(rootLayer.subLayerPaths)
if anon.identifier in paths:
    paths.remove(anon.identifier)
    rootLayer.subLayerPaths = paths
    print("Removed anonymous sublayer.")
else:
    print("Anonymous sublayer not found in root sublayers.")

print("Final sublayers:")
for p in rootLayer.subLayerPaths:
    print(" -", p)

print("layer_create_edit_revert.py finished.")

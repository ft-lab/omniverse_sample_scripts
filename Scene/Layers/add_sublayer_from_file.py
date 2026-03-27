from pxr import Sdf
import omni.usd
import os

"""
Sample: Register an existing (or newly created) USD file as a sublayer
without using Sdf.Layer.CreateAnonymous().

Behavior:
 - If the current stage is saved to disk, create (or reuse) a usd file
   named `sublayer_from_file.usd` in the same directory and append it to
   the root layer's subLayerPaths.
 - By default this sample performs cleanup: it removes the appended
   sublayer from rootLayer.subLayerPaths and deletes the file if it was
   created by this script. Set `CLEANUP=False` to keep the sublayer.
"""

CLEANUP = True

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()
print(f"Root layer: {rootLayer.identifier}")

try:
    root_real = rootLayer.realPath
except Exception:
    root_real = None

if not root_real:
    print("Root layer has no realPath — save the stage first to use this sample.")
    raise RuntimeError("Root layer has no realPath")

folder = os.path.dirname(root_real)
sublayer_path = os.path.join(folder, "sublayer_from_file.usd")
created = False

# If the file does not exist, create a new persistent layer file.
if not os.path.exists(sublayer_path):
    layer = Sdf.Layer.CreateNew(sublayer_path)
    if layer:
        print(f"Created new sublayer file: {sublayer_path}")
        created = True
    else:
        print(f"Failed to create sublayer file: {sublayer_path}")
        raise RuntimeError(f"Failed to create sublayer file: {sublayer_path}")
else:
    print(f"Using existing sublayer file: {sublayer_path}")

# Append the sublayer path to root layer (if not already present)
paths = list(rootLayer.subLayerPaths)
if sublayer_path not in paths:
    paths.append(sublayer_path)
    rootLayer.subLayerPaths = paths
    print(f"Appended sublayer: {sublayer_path}")
else:
    print(f"Sublayer already present: {sublayer_path}")

# Optionally clean up the change to avoid persisting modifications
if CLEANUP:
    paths = list(rootLayer.subLayerPaths)
    if sublayer_path in paths:
        paths.remove(sublayer_path)
        rootLayer.subLayerPaths = paths
        print("Removed appended sublayer (cleanup)")
    if created:
        try:
            os.remove(sublayer_path)
            print(f"Deleted created sublayer file: {sublayer_path}")
        except Exception as e:
            print(f"Failed to delete created sublayer file: {e}")

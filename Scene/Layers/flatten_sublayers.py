from pxr import Usd
import omni.usd
import omni.kit.commands

"""
Flatten sublayers into the root layer using the Omniverse Kit command.

This sample calls the Omniverse application command `FlattenLayers`
via `omni.kit.commands.execute(...)`. This is an application-level
operation (Kit) — not pure USD API.

Usage: run inside Omniverse (Kit) context.
"""

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()

print("Before flatten, sublayers:")
for p in rootLayer.subLayerPaths:
    print(" -", p)

# Call the Omniverse Kit command that performs a proper flatten/merge
# of sublayers into the root layer. This delegates the merge operation
# to the Kit application which knows how to compose and write the
# resulting root layer contents.
omni.kit.commands.execute("FlattenLayers")

print("After flatten, sublayers:")
for p in rootLayer.subLayerPaths:
    print(" -", p)


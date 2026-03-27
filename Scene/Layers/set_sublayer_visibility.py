from pathlib import Path
from pxr import Usd
import omni.usd
import omni.kit.commands

"""
Set visibility (mute) for sublayers using Omniverse Kit command.

This sample uses `omni.kit.commands.execute("SetLayerMuteness", ...)`,
which is an Omniverse Kit (application) command — not a core USD API.
That command mutes/unmutes a layer in the Kit application so it becomes
effectively invisible/visible in the UI. We convert relative sublayer
paths to absolute paths based on the root layer's realPath before
calling the command.

Usage: run inside Omniverse (Kit) context.
"""


def convert_to_absolute_path(stage: Usd.Stage, path: str) -> str:
    root_layer = stage.GetRootLayer()
    if not root_layer:
        return None
    try:
        real_path = root_layer.realPath
    except Exception:
        real_path = None
    if not real_path:
        return None
    real_dir = Path(real_path).parent
    return str(real_dir.joinpath(path)).replace("\\", "/")


def get_sublayer_absolute_paths(stage: Usd.Stage) -> list:
    root_layer = stage.GetRootLayer()
    if not root_layer:
        return []
    try:
        real_path = root_layer.realPath
    except Exception:
        real_path = None
    if not real_path:
        return []
    real_dir = Path(real_path).parent
    abs_paths = []
    for p in root_layer.subLayerPaths:
        abs_paths.append(str(real_dir.joinpath(p)).replace("\\", "/"))
    return abs_paths


def set_sublayer_visibility(stage: Usd.Stage, sublayer_path: str, visible: bool) -> str:
    root_layer = stage.GetRootLayer()
    if not root_layer:
        raise RuntimeError("Root layer not found")

    # Convert to absolute path if relative
    abs_path = convert_to_absolute_path(stage, sublayer_path)
    if abs_path:
        target = abs_path
    else:
        target = sublayer_path

    # Verify the sublayer exists
    abs_list = get_sublayer_absolute_paths(stage)
    if target not in abs_list:
        raise RuntimeError(f"Specified sublayer not found: {target}")

    # Use Omniverse Kit command to set layer muteness (mute = not visible)
    omni.kit.commands.execute("SetLayerMuteness", layer_identifier=target, muted=not visible)
    return target



stage = omni.usd.get_context().get_stage()
paths = get_sublayer_absolute_paths(stage)
if not paths:
    print("No sublayers to set visibility for")
else:
    for p in paths:
        print("Setting invisible for:", p)
        try:
            fp = set_sublayer_visibility(stage, p, False)
            print("Set invisible:", fp)
        except Exception as e:
            print("Failed to set visibility for", p, ":", e)

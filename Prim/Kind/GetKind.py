import omni.usd
from pxr import Usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        continue

    v = Usd.ModelAPI(prim).GetKind()
    print(f'[ {prim.GetName()} ] Kind = {v}')


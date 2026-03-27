import omni.usd
from pxr import Kind, Usd

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

    # Change the value of Kind in Prim to Component.
    Usd.ModelAPI(prim).SetKind(Kind.Tokens.component)

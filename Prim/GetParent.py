import omni.usd

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

    # Get parent prim.
    parentPrim = prim.GetParent()
    if parentPrim.IsValid():
        print(f"[ {prim.GetPath().pathString} ]")
        print(f"  Parent : {parentPrim.GetPath().pathString}")

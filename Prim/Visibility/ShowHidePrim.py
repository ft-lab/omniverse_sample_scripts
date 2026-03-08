from pxr import UsdGeom

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# Toggle show/hide.
for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        continue

    # Get visibility.
    primImageable = UsdGeom.Imageable(prim)
    if primImageable.GetVisibilityAttr().Get() == UsdGeom.Tokens.inherited:
        # Set hide.
        primImageable.GetVisibilityAttr().Set(UsdGeom.Tokens.invisible)
    else:
        # Set show (inherited).
        primImageable.GetVisibilityAttr().Set(UsdGeom.Tokens.inherited)

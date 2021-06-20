from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# Toggle show/hide.
for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue

    # Get visibility.
    primImageable = UsdGeom.Imageable(prim)
    if primImageable.GetVisibilityAttr().Get() == 'inherited':
        # Set hide.
        primImageable.GetVisibilityAttr().Set('invisible')
    else:
        # Set show (inherited).
        primImageable.GetVisibilityAttr().Set('inherited')

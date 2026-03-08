from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue

    # Get visibility.
    primImageable = UsdGeom.Imageable(prim)
    showF = (primImageable.ComputeVisibility() != UsdGeom.Tokens.invisible)

    if primImageable.GetVisibilityAttr().Get() == UsdGeom.Tokens.inherited:
        print(f'[ {prim.GetName()} ] inherited  visible = {showF}')
    else:
        print(f'[ {prim.GetName()} ] invisible  visible = {showF}')


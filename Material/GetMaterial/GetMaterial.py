from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)

    # Get Material.
    rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
    pathList = rel.GetTargets()

    print('[ ' + prim.GetName() + ' ]')
    for mTargetPath in pathList:
        print('  material : ' + mTargetPath.pathString)

        material = UsdShade.Material(stage.GetPrimAtPath(mTargetPath))
        print(material)


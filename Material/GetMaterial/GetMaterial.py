from pxr import UsdShade

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)

    # Get Material.
    rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
    pathList = rel.GetTargets()

    print(f"[ {prim.GetName()} ]")
    for mTargetPath in pathList:
        print(f"  material : {mTargetPath.pathString}")

        material = UsdShade.Material(stage.GetPrimAtPath(mTargetPath))
        print(material)


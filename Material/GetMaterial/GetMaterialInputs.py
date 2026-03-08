from pxr import UsdShade

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if not prim.IsA(UsdShade.Material):
        continue

    print(f"[ {prim.GetPath().pathString} ]")

    # Get Shader of Material and input parameters.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.IsA(UsdShade.Shader):
            shaderPrim = UsdShade.Shader(cPrim)

            mInputs = shaderPrim.GetInputs()
            for inputV in mInputs:
                baseName = inputV.GetBaseName()
                typeName = inputV.GetTypeName()
                print(f"    [{baseName}] ({typeName})")

                v = inputV.Get()
                print(f"      {type(v)} ==> {v}")



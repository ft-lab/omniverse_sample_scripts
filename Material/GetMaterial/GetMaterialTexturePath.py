from pxr import UsdShade

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if not prim.IsA(UsdShade.Material):
        continue

    # List textures referenced by Material.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.IsA(UsdShade.Shader):
            shaderPrim = UsdShade.Shader(cPrim)

            print(f"[{shaderPrim.GetPath().pathString}]")

            mInputs = shaderPrim.GetInputs()
            for inputV in mInputs:
                baseName = inputV.GetBaseName()
                typeName = inputV.GetTypeName()
                if typeName == "asset":
                    v = inputV.Get()    # Sdf.AssetPath
                    if v.path != "":
                        #   v.path         ... display path.
                        #   v.resolvedPath ... absolute path.
                        print(f"  {baseName}")
                        print(f"      path [ {v.path} ]")
                        print(f"      resolvedPath [ {v.resolvedPath} ]")


from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.GetTypeName() != "Material":
        continue

    # List textures referenced by Material.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.GetTypeName() == "Shader":
            shaderPrim = UsdShade.Shader(cPrim)

            print(f"[{shaderPrim.GetPath().pathString}]")

            mInputs = shaderPrim.GetInputs()
            for inputV in mInputs:
                baseName = inputV.GetBaseName()
                typeName = inputV.GetTypeName()
                if typeName == "asset":
                    v = inputV.Get()    # Sdf.AssetPath
                    if v.path != "":
                        print(f"  {baseName}")
                        print(f"      path [ {v.path} ]")
                        print(f"      resolvedPath [ {v.resolvedPath} ]")


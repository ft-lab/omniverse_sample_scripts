from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.GetTypeName() != "Material":
        continue

    print("[" + prim.GetPath().pathString + "]")

    # Get Shader of Material and input parameters.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.GetTypeName() == "Shader":
            shaderPrim = UsdShade.Shader(cPrim)

            mInputs = shaderPrim.GetInputs()
            for inputV in mInputs:
                baseName = inputV.GetBaseName()
                typeName = inputV.GetTypeName()
                print("    [" + baseName + "] (" + str(typeName) + ")")

                v = inputV.Get()
                print("      " + str(type(v)) + " ==> " + str(v))



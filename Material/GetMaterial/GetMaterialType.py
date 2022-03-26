from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.GetTypeName() != "Material":
        continue

    # Get Shader of Material and input parameters.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.GetTypeName() == "Shader":
            shaderPrim = UsdShade.Shader(cPrim)

            # In the case of UsdPreviewSurface, ImplementationSource is "id".
            # In the case of MDL, the ImplementationSource is "sourceAsset".
            sourceV = shaderPrim.GetImplementationSource()
            print("implementationSource : " + sourceV)
            if sourceV == "id":
                attr = shaderPrim.GetIdAttr()
                idValue = attr.Get()    # "UsdPreviewSurface"
                print(attr.GetName() + " : " + idValue)

            # Get MDL information.
            if sourceV == "sourceAsset":
                assetPath = shaderPrim.GetSourceAsset("mdl")
                print("assetPath : " + assetPath.path)

                subIdentifier = shaderPrim.GetSourceAssetSubIdentifier("mdl")
                print("sourceAsset:subIdentifier : " + subIdentifier)



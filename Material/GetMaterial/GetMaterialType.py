from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# Get material type (UsdPreviewSurface/OmniPBR/CustomMDL etc.)
def GetMaterialType (path : str):
    prim = stage.GetPrimAtPath(path)
    if prim.GetTypeName() != "Material":
        return ""
    
    materialTypeName = ""
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.GetTypeName() == "Shader":
            shaderPrim = UsdShade.Shader(cPrim)

            # In the case of UsdPreviewSurface, ImplementationSource is "id".
            # In the case of MDL, the ImplementationSource is "sourceAsset".
            sourceV = shaderPrim.GetImplementationSource()
            if sourceV == "id":
                attr = shaderPrim.GetIdAttr()
                idValue = attr.Get()    # "UsdPreviewSurface"
                if idValue == "UsdPreviewSurface":
                    materialTypeName = idValue

            # Get MDL information.
            if sourceV == "sourceAsset":
                # Sdf.AssetPath
                #   assetPath.path ... display path.
                #   assetPath.resolvedPath ... absolute path.
                assetPath = shaderPrim.GetSourceAsset("mdl")

                # MDL name.
                subIdentifier = shaderPrim.GetSourceAssetSubIdentifier("mdl")

                if subIdentifier != "":
                    materialTypeName = subIdentifier
                else:
                    materialTypeName = assetPath.resolvedPath

            if materialTypeName != "":
                break

    return materialTypeName

# -----------------------------------.
for path in paths:
    materialTypeName = GetMaterialType(path)

    if materialTypeName != "":
        print(f"{path} : {materialTypeName}")


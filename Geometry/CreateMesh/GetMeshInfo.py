from pxr import UsdGeom, UsdShade

# ---------------------------------------.
# Dump mesh data.
# ---------------------------------------.
def DumpMeshData(prim):
    if prim.IsA(UsdGeom.Mesh):
        m = UsdGeom.Mesh(prim)

        # Get prim name.
        name = prim.GetName()

        # Get prim path.
        path = prim.GetPath().pathString

        # Get show/hide.
        showF = (m.ComputeVisibility() == UsdGeom.Tokens.inherited)

        # Get the number of faces of Mesh.
        facesCou = len(m.GetFaceVertexCountsAttr().Get())

        # Get number of normals.
        normalsCou = len(m.GetNormalsAttr().Get()) if m.GetNormalsAttr() and m.GetNormalsAttr().Get() else 0
        normalsInterpolation = m.GetNormalsInterpolation()

        # Total number of vertices.
        versCou = len(m.GetPointsAttr().Get())

        # Get UV.
        # USD 22.11 : The specification has been changed to use UsdGeom.PrimvarsAPI.
        primvarsAPI = UsdGeom.PrimvarsAPI(prim)
        uvsCou = 0
        uvInterpolation = ""
        primvar = primvarsAPI.GetPrimvar("st")
        if primvar.IsDefined():
            typeName = str(primvar.GetTypeName().arrayType)
            if typeName == "float2[]" or typeName == "texCoord2f[]":
                uvsCou = len(primvar.Get()) if not primvar.IsIndexed() else len(primvar.GetIndices())
                uvInterpolation = primvar.GetInterpolation()

        if normalsCou == 0:
            primvar = primvarsAPI.GetPrimvar(UsdGeom.Tokens.normals)
            if primvar.IsDefined():
                typeName = str(primvar.GetTypeName().arrayType)
                if typeName == "normal3f[]":
                    normalsCou = len(primvar.Get()) if not primvar.IsIndexed() else len(primvar.GetIndices())
                    normalsInterpolation = primvar.GetInterpolation()

        # Get Material.
        rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
        pathList = rel.GetTargets()

        print(f"[ {name} ] {path}")
        print(f"Show   : {showF}")
        print(f"Points : {versCou}")
        print(f"Faces  : {facesCou}")
        print(f"normals : {normalsCou}")
        print(f"normals interpolation : {normalsInterpolation}")
        print(f"uvs    : {uvsCou}")
        print(f"uvs interpolation : {uvInterpolation}")

        if len(pathList) > 0:
            print("Material : ")
            for mPath in pathList:
                print(f"     {mPath.pathString}")

        print("")

# ---------------------------------------.
# Traverse the hierarchy.
# ---------------------------------------.
def TraverseHierarchy(prim):
    DumpMeshData(prim)

    # Recursively traverse the hierarchy.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        TraverseHierarchy(cPrim)

# ----------------------------------------------------.
# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    TraverseHierarchy(prim)
   

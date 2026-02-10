from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# ---------------------------------------.
# Dump mesh data.
# ---------------------------------------.
def DumpMeshData (prim):
    if prim.IsA(UsdGeom.Mesh):
        m = UsdGeom.Mesh(prim)

        # Get prim name.
        name = prim.GetName()

        # Get prim path.
        path = prim.GetPath().pathString

        # Get show/hide.
        showF = (m.ComputeVisibility() == "inherited")

        # Get the number of faces of Mesh.
        facesCou = len(m.GetFaceVertexCountsAttr().Get())

        # Get number of normals.
        normalsCou = len(m.GetNormalsAttr().Get()) if m.GetNormalsAttr() and m.GetNormalsAttr().Get() else 0

        # Total number of vertices.
        versCou = len(m.GetPointsAttr().Get())

        # Get UV.
        # USD 22.11 : The specification has been changed to use UsdGeom.PrimvarsAPI.
        primvarsAPI = UsdGeom.PrimvarsAPI(prim)
        primvars = primvarsAPI.GetPrimvars()

        uvsCou = 0
        uvlayersCou = 0
        for primvar in primvars:
            typeName = str(primvar.GetTypeName().arrayType)
            if typeName == "float2[]" or typeName == "texCoord2f[]":
                # 'st'
                pName = primvar.GetPrimvarName()
                uvlayersCou += 1
                uvsCou = len(primvar.Get())

        if normalsCou == 0:
            for primvar in primvars:
                typeName = str(primvar.GetTypeName().arrayType)
                name = primvar.GetName()
                if name == "primvars:normals" and typeName == "normal3f[]":
                    # 'normals'
                    pName = primvar.GetPrimvarName()
                    normalsCou = len(primvar.Get())
                    break

        # Get Material.
        rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
        pathList = rel.GetTargets()

        print(f"[ {name} ] {path}")
        print(f"Show   : {showF}")
        print(f"Points : {versCou}")
        print(f"Faces  : {facesCou}")
        print(f"uvs    : {uvsCou}")
        print(f"normals : {normalsCou}")
        print(f"UV sets : {uvlayersCou}")

        if len(pathList) > 0:
            print("Material : ")
            for mPath in pathList:
                print(f"     {mPath.pathString}")

        print("")

# ---------------------------------------.
# Traverse the hierarchy.
# ---------------------------------------.
def TraverseHierarchy (prim):
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
   

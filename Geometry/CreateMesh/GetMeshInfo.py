from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# ---------------------------------------.
# Dump mesh data.
# ---------------------------------------.
def DumpMeshData (prim):
    typeName = prim.GetTypeName()

    if typeName == 'Mesh':
        m = UsdGeom.Mesh(prim)

        # Get prim name.
        name = prim.GetName()

        # Get prim path.
        path = prim.GetPath().pathString

        # Get show/hide.
        showF = (m.ComputeVisibility() == 'inherited')

        # Get the number of faces of Mesh.
        facesCou = len(m.GetFaceVertexCountsAttr().Get())

        # Total number of vertices.
        versCou = len(m.GetPointsAttr().Get())

        # Get UV.
        uvlayersCou = 0
        primvars = m.GetPrimvars()
        for primvar in primvars:
            if str(primvar.GetTypeName().arrayType) == 'float2[]':
                # 'st'
                pName = primvar.GetPrimvarName()
                uvlayersCou += 1

        # Get Material.
        rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
        pathList = rel.GetTargets()

        print("[ " + name + " ]  " + path)
        print("Show   : " + str(showF))
        print("Points : " + str(versCou))
        print("Faces  : " + str(facesCou))
        print("UV sets : " + str(uvlayersCou))

        if len(pathList) > 0:
            print("Material : ")
            for mPath in pathList:
                print("    " + mPath.pathString)

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
   

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# ---------------------------------------.
# traverse the hierarchy.
# ---------------------------------------.
def TraverseHierarchy_number (depth, prim):
    if prim.IsValid() == None:
        return 0
    typeName = prim.GetTypeName()

    allCou = 0
    if typeName == 'Mesh':
        m = UsdGeom.Mesh(prim)

        # If it is displayed.
        if m.ComputeVisibility() == 'inherited':
            # Get the number of faces of Mesh.
            allCou += len(m.GetFaceVertexCountsAttr().Get())

    # Recursively traverse the hierarchy.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        allCou += TraverseHierarchy_number(depth + 1, cPrim)

    return allCou

# ---------------------------------------.

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Get root path.
rootPath = '/'
if defaultPrim.IsValid():
    rootPath = defaultPrim.GetPath().pathString

# traverse the hierarchy.
tPrim = stage.GetPrimAtPath(rootPath)
allFacesCou = TraverseHierarchy_number(0, tPrim)
print("Number of all faces : " + str(allFacesCou))


from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# ---------------------------------------.
# traverse the hierarchy.
# ---------------------------------------.
def TraverseHierarchy (depth, prim):
    if prim.IsValid() == None:
        return

    indentStr = ''
    for i in range(depth):
        indentStr += '    '
    
    # Print Prim information.
    name = prim.GetName()
    typeName = prim.GetTypeName()
    s = indentStr + '[ ' + name + ' ]'
    s += ' type : ' + typeName

    # If hidden.
    if UsdGeom.Imageable(prim).ComputeVisibility() == 'invisible':
        s += ' ** Hide **'

    print(s)

    if typeName == 'Mesh':
        # Get the number of faces of Mesh.
        m = UsdGeom.Mesh(prim)

        faceCount = len(m.GetFaceVertexCountsAttr().Get())
        print(indentStr + '    Face count : ' + str(faceCount))

    # Recursively traverse the hierarchy.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        TraverseHierarchy(depth + 1, cPrim)

# ---------------------------------------.

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
print("--- Default prim ---")
defaultPrim = stage.GetDefaultPrim()
if defaultPrim.IsValid():
    print("DefaultPrim(Name) : " + defaultPrim.GetName())
    print("DefaultPrim(Path) : " + defaultPrim.GetPath().pathString)
else:
    print("Default Prim does not exist.")
print("")

# Get root path.
rootPath = '/'
if defaultPrim.IsValid():
    rootPath = defaultPrim.GetPath().pathString
print("Root path : " + rootPath)
print("")

# traverse the hierarchy.
tPrim = stage.GetPrimAtPath(rootPath)
print("--- Hierarchy ---")
TraverseHierarchy(0, tPrim)
print("")


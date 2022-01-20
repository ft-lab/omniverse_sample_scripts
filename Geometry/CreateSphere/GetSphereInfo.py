from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf

xformCache = UsdGeom.XformCache(0)

# ---------------------------------------.
# Dump sphere data.
# ---------------------------------------.
def DumpSphereData (prim):
    typeName = prim.GetTypeName()

    if typeName == 'Sphere':
        sphereGeom = UsdGeom.Sphere(prim)

        # Get prim name.
        name = prim.GetName()

        # Get prim path.
        path = prim.GetPath().pathString

        # Get show/hide.
        showF = (sphereGeom.ComputeVisibility() == 'inherited')

        # Decompose transform.
        globalPose = xformCache.GetLocalToWorldTransform(prim)
        translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

        # Get radius.
        r = sphereGeom.GetRadiusAttr().Get()

        # Get Material.
        rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
        pathList = rel.GetTargets()

        print("[ " + name + " ]  " + path)
        print("Show    : " + str(showF))
        print ("Radius : " + str(r * scale[0]) + " , " + str(r * scale[1]) + " , " + str(r * scale[2]))

        if len(pathList) > 0:
            print("Material : ")
            for mPath in pathList:
                print("    " + mPath.pathString)

        print("")

# ---------------------------------------.
# Traverse the hierarchy.
# ---------------------------------------.
def TraverseHierarchy (prim):
    DumpSphereData(prim)

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
   

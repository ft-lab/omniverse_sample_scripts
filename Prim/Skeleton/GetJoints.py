from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# -------------------------------------------------------------------.
# Traverse.
# -------------------------------------------------------------------.
def Traverse (prim):
    if prim.IsValid() == None:
        return

    # For Skeleton, get the Joints information.
    if prim.GetTypeName() == 'Skeleton':
        jointAttr          = prim.GetAttribute("joints")
        bindTransformsAttr = prim.GetAttribute("bindTransforms")
        restTransformsAttr = prim.GetAttribute("restTransforms")

        if jointAttr.IsValid() and bindTransformsAttr.IsValid() and restTransformsAttr.IsValid():
            jCou = len(jointAttr.Get())

            print("[ " + prim.GetPath().pathString + " ]")

            for i in range(jCou):
                jointName     = jointAttr.Get()[i]
                bindTransform = bindTransformsAttr.Get()[i]
                restTransform = restTransformsAttr.Get()[i]

                print(str(i) + " : " + jointName)
                print("    bindTransform : " + str(bindTransform))
                print("    restTransform : " + str(restTransform))

    # Recursively traverse the hierarchy.
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        Traverse(cPrim)

# -------------------------------------------------------------------.
for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    Traverse(prim)






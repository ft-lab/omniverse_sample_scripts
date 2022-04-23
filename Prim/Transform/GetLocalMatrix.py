from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

xformCache = UsdGeom.XformCache(0)

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        # Calc local matrix.
        curM = xformCache.GetLocalToWorldTransform(prim)
        parentPrim = prim.GetParent()
        matrix = curM * xformCache.GetLocalToWorldTransform(parentPrim).GetInverse()
        print(matrix)




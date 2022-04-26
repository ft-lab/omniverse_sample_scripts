from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.timeline

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        pV = Gf.Vec3f(10.0, 20.0, 0.0)
        pivot = prim.GetAttribute("xformOp:translate:pivot").Get()

        if pivot != None:
            # Specify a value for each type.
            if type(pivot) == Gf.Vec3f:
                prim.GetAttribute("xformOp:translate:pivot").Set(Gf.Vec3f(pV))
            elif type(pivot) == Gf.Vec3d:
                prim.GetAttribute("xformOp:translate:pivot").Set(Gf.Vec3d(pV))
        else:
            # xformOpOrder is also updated.
            xformAPI = UsdGeom.XformCommonAPI(prim)
            xformAPI.SetPivot(Gf.Vec3f(pV))


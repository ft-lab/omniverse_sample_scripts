from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.timeline

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# --------------------------------------------------.
# Set translate.
# --------------------------------------------------.
def _setTranslate (prim : Usd.Prim, tV : Gf.Vec3f):
    if prim == None:
        return

    trans = prim.GetAttribute("xformOp:translate").Get()
    if trans != None:
        # Specify a value for each type.
        if type(trans) == Gf.Vec3f:
            prim.GetAttribute("xformOp:translate").Set(Gf.Vec3f(tV))
        elif type(trans) == Gf.Vec3d:
            prim.GetAttribute("xformOp:translate").Set(Gf.Vec3d(tV))
    else:
        # xformOpOrder is also updated.
        xformAPI = UsdGeom.XformCommonAPI(prim)
        xformAPI.SetTranslate(Gf.Vec3d(tV))

# -------------------------------------------------.
for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        tV = Gf.Vec3f(10, 20, 30)
        _setTranslate(prim, tV)

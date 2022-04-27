from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.timeline

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# --------------------------------------------------.
# Set pivot.
# --------------------------------------------------.
def _setPivot (prim : Usd.Prim, pV : Gf.Vec3f):
    pivot = prim.GetAttribute("xformOp:translate:pivot").Get()

    if pivot != None:
        # Specify a value for each type.
        if type(pivot) == Gf.Vec3f:
            prim.GetAttribute("xformOp:translate:pivot").Set(Gf.Vec3f(pV))
        elif type(pivot) == Gf.Vec3d:
            prim.GetAttribute("xformOp:translate:pivot").Set(Gf.Vec3d(pV))
    else:
        # xformOpOrder is also updated.
        # ["xformOp:translate", "xformOp:translate:pivot", "xformOp:rotateXYZ", "xformOp:scale", "!invert!xformOp:translate:pivot"]
        # The following do not work correctly?
        #xformAPI = UsdGeom.XformCommonAPI(prim)
        #xformAPI.SetPivot(Gf.Vec3f(pV))

        prim.CreateAttribute("xformOp:translate:pivot", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(pV))

        # ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale", "xformOp:translate:pivot", "!invert!xformOp:translate:pivot"]
        transformOrder = prim.GetAttribute("xformOpOrder").Get()
        orderList = []
        for sV in transformOrder:
            orderList.append(sV)
        orderList.append("xformOp:translate:pivot")
        orderList.append("!invert!xformOp:translate:pivot")
        prim.GetAttribute("xformOpOrder").Set(orderList)

# --------------------------------------------------.
for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        pV = Gf.Vec3f(10.0, 20.0, 0.0)
        _setPivot(prim, pV)

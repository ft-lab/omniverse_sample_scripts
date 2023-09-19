from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.timeline

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# --------------------------------------------------.
# Set Rotate.
# --------------------------------------------------.
def _setRotate (prim : Usd.Prim, rV : Gf.Vec3f):
    if prim == None:
        return

    # Get rotOrder.
    # If rotation does not exist, rotOrder = UsdGeom.XformCommonAPI.RotationOrderXYZ.
    xformAPI = UsdGeom.XformCommonAPI(prim)
    time_code = Usd.TimeCode.Default()
    translation, rotation, scale, pivot, rotOrder = xformAPI.GetXformVectors(time_code)

    # If with orientation, specify rotation with quat.
    tV = prim.GetAttribute("xformOp:orient")
    if tV.IsValid():
        rotX = Gf.Rotation(Gf.Vec3d(1, 0, 0), rV[0])
        rotY = Gf.Rotation(Gf.Vec3d(0, 1, 0), rV[1])
        rotZ = Gf.Rotation(Gf.Vec3d(0, 0, 1), rV[2])
        rotXYZ = rotX * rotY * rotZ
        if type(tV.Get()) == Gf.Quatd:
            tV.Set(rotXYZ.GetQuat())
        elif type(tV.Get()) == Gf.Quatf:
            tV.Set(Gf.Quatf(rotXYZ.GetQuat()))

    else:
        # Convert rotOrder to "xformOp:rotateXYZ" etc.
        t = xformAPI.ConvertRotationOrderToOpType(rotOrder)
        rotateAttrName = "xformOp:" + UsdGeom.XformOp.GetOpTypeToken(t)

        # Set rotate.
        rotate = prim.GetAttribute(rotateAttrName).Get()
        if rotate != None:
            # Specify a value for each type.
            if type(rotate) == Gf.Vec3f:
                prim.GetAttribute(rotateAttrName).Set(Gf.Vec3f(rV))
            elif type(rotate) == Gf.Vec3d:
                prim.GetAttribute(rotateAttrName).Set(Gf.Vec3d(rV))
        else:
            # xformOpOrder is also updated.
            xformAPI.SetRotate(Gf.Vec3f(rV), rotOrder)

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print(f"[ {prim.GetName()} ]")

        rV = Gf.Vec3f(10.0, 25.0, 12.0)
        _setRotate(prim, rV)


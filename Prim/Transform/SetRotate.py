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

        rV = Gf.Vec3f(10.0, 25.0, 12.0)

        # Get rotOrder.
        # If rotation does not exist, rotOrder = UsdGeom.XformCommonAPI.RotationOrderXYZ.
        xformAPI = UsdGeom.XformCommonAPI(prim)
        translation, rotation, scale, pivot, rotOrder = xformAPI.GetXformVectors(time_code)

        if rotOrder != None:
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




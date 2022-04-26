from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.timeline

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

time_code = Usd.TimeCode.Default()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        # Get transform.
        # However, the type that can be obtained here is different from the actual Type.
        xformAPI = UsdGeom.XformCommonAPI(prim)
        translation, rotation, scale, pivot, rotOrder = xformAPI.GetXformVectors(time_code)

        print("** GetXformVectors **")

        print("translation : " + str(type(translation)) + " " + str(translation))
        print("rotation : " + str(type(rotation)) + " " + str(rotation))
        print("scale : " + str(type(scale)) + " " + str(scale))
        print("pivot : " + str(type(pivot)) + " " + str(pivot))
        print("rotOrder : " + str(type(rotOrder)) + " " + str(rotOrder))

        print("** prim.GetAttribute **")

        trans = prim.GetAttribute("xformOp:translate").Get()
        print("trans : " + str(type(trans)) + " " + str(trans))

        # Convert rotOrder to "xformOp:rotateXYZ" etc.
        t = xformAPI.ConvertRotationOrderToOpType(rotOrder)
        rotateAttrName = "xformOp:" + UsdGeom.XformOp.GetOpTypeToken(t)

        rotate = prim.GetAttribute(rotateAttrName).Get()
        print("rotate (" + rotateAttrName + ") : " + str(type(rotate)) + " " + str(rotate))

        scale = prim.GetAttribute("xformOp:scale").Get()
        print("scale : " + str(type(scale)) + " " + str(scale))
        
        pivot = prim.GetAttribute("xformOp:translate:pivot").Get()
        print("pivot : " + str(type(pivot)) + " " + str(pivot))

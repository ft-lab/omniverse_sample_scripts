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
        print(f"[ {prim.GetName()} ]")

        # Get transform.
        # However, the type that can be obtained here is different from the actual Type.
        xformAPI = UsdGeom.XformCommonAPI(prim)
        translation, rotation, scale, pivot, rotOrder = xformAPI.GetXformVectors(time_code)

        print("** GetXformVectors **")

        print(f"translation : {type(translation)} {translation}")
        print(f"rotation : {type(rotation)} {rotation}")
        print(f"scale : {type(scale)} {scale}")
        print(f"pivot : {type(pivot)} {pivot}")
        print(f"rotOrder : {type(rotOrder)} {rotOrder}")

        print("** prim.GetAttribute **")

        trans = prim.GetAttribute("xformOp:translate").Get()
        print(f"trans : {type(trans)} {trans}")

        # Convert rotOrder to "xformOp:rotateXYZ" etc.
        t = xformAPI.ConvertRotationOrderToOpType(rotOrder)
        rotateAttrName = "xformOp:" + UsdGeom.XformOp.GetOpTypeToken(t)

        rotate = prim.GetAttribute(rotateAttrName).Get()
        print(f"rotate ({rotateAttrName}) : {type(rotate)} {rotate}")

        scale = prim.GetAttribute("xformOp:scale").Get()
        print(f"scale : {type(scale)} {scale}")
        
        pivot = prim.GetAttribute("xformOp:translate:pivot").Get()
        print(f"pivot : {type(pivot)} {pivot}")

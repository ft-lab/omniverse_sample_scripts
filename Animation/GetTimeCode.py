from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get TimeCode.
print("Start TimeCode : " + str(stage.GetStartTimeCode()))
print("End TimeCode : " + str(stage.GetEndTimeCode()))

# Get frame rate.
print("TimeCodesPerSecond : " + str(stage.GetTimeCodesPerSecond()))


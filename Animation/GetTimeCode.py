from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get TimeCode.
print(f"Start TimeCode : {stage.GetStartTimeCode()}")
print(f"End TimeCode : {stage.GetEndTimeCode()}")

# Get frame rate.
print(f"TimeCodesPerSecond : {stage.GetTimeCodesPerSecond()}")


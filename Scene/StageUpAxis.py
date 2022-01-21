from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get UpAxis.
upAxis = UsdGeom.GetStageUpAxis(stage)

if upAxis == UsdGeom.Tokens.x:
    print("UpAxis : X")
elif upAxis == UsdGeom.Tokens.y:
    print("UpAxis : Y")
elif upAxis == UsdGeom.Tokens.z:
    print("UpAxis : Z")

# Set UpAxis (Y-Up).
try:
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
except Exception as e:
    print(e)


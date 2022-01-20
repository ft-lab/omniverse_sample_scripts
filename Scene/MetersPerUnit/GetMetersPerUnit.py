from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get metersPerUnit (default : 0.01).
metersPerUnit = UsdGeom.GetStageMetersPerUnit(stage)
print(metersPerUnit)

# Set metersPerUnit.
UsdGeom.SetStageMetersPerUnit(stage, 0.01)


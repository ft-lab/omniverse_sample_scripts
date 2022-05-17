from pxr import Usd, UsdGeom, UsdPhysics, UsdLux, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create distant light.
pathName = "/World/light"
light = UsdLux.DistantLight.Define(stage, pathName)

# Set intensity.
light.CreateIntensityAttr(100.0)

# Set color.
light.CreateColorAttr(Gf.Vec3f(1.0, 0.5, 0.2))

# Set Exposure.
light.CreateExposureAttr(0.0)

# cone angle.
UsdLux.ShapingAPI(light).CreateShapingConeAngleAttr(180.0)


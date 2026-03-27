from pxr import UsdLux, Gf
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create distant light.
pathName = "/World/distantLight"
light = UsdLux.DistantLight.Define(stage, pathName)

# Set intensity.
light.CreateIntensityAttr(100.0)

# Set color.
light.CreateColorAttr(Gf.Vec3f(1.0, 0.5, 0.2))

# Set Exposure.
light.CreateExposureAttr(0.0)

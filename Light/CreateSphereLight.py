from pxr import Usd, UsdGeom, UsdLux, Gf
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create sphere light.
pathName = "/World/sphereLight"
light = UsdLux.SphereLight.Define(stage, pathName)

# Set Radius.
light.CreateRadiusAttr(20.0)

# Set intensity.
light.CreateIntensityAttr(50000.0)

# Set color.
light.CreateColorAttr(Gf.Vec3f(1.0, 0.9, 0.8))

# Set Exposure.
light.CreateExposureAttr(0.0)

# cone angle.
shapingAPI = UsdLux.ShapingAPI(light)
shapingAPI.CreateShapingConeAngleAttr(180.0)
shapingAPI.Apply(light.GetPrim())  # Register ShapingAPI as a schema in prim.

# Move to (0, 50, 0)
xformable = UsdGeom.Xformable(light.GetPrim())
xformable.AddTranslateOp().Set(Gf.Vec3d(0.0, 50.0, 0.0))

# Compute extent.
boundable = UsdGeom.Boundable(light.GetPrim())
extent = boundable.ComputeExtent(Usd.TimeCode(0))

# Set Extent.
light.CreateExtentAttr(extent)

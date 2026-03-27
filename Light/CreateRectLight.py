from pxr import Usd, UsdGeom, UsdLux, Gf
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create rect light.
pathName = "/World/rectLight"
light = UsdLux.RectLight.Define(stage, pathName)

# Set Width and Height.
light.CreateWidthAttr(20.0)
light.CreateHeightAttr(20.0)

# Set intensity.
light.CreateIntensityAttr(10000.0)

# Set color.
light.CreateColorAttr(Gf.Vec3f(1.0, 0.9, 0.8))

# Set Exposure.
light.CreateExposureAttr(0.0)

# cone angle.
shapingAPI = UsdLux.ShapingAPI(light)
shapingAPI.CreateShapingConeAngleAttr(180.0)
shapingAPI.Apply(light.GetPrim())  # Register ShapingAPI as a schema in prim.

# Apply downward rotation to transform
xformable = UsdGeom.Xformable(light.GetPrim())
xformable.AddRotateXOp().Set(270.0)

# Compute extent.
boundable = UsdGeom.Boundable(light.GetPrim())
extent = boundable.ComputeExtent(Usd.TimeCode(0))

# Set Extent.
light.CreateExtentAttr(extent)

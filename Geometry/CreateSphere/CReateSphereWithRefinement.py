from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create sphere.
pathName = '/World/sphere'
sphereGeom = UsdGeom.Sphere.Define(stage, pathName)

# Set radius.
sphereGeom.CreateRadiusAttr(5.0)

# Set color.
sphereGeom.CreateDisplayColorAttr([(1.0, 0.0, 0.0)])

# Set position.
UsdGeom.XformCommonAPI(sphereGeom).SetTranslate((0.0, 5.0, 0.0))

# Set refinement.
objPrim = stage.GetPrimAtPath(pathName)
objPrim.CreateAttribute('refinementEnableOverride', Sdf.ValueTypeNames.Bool).Set(True)
objPrim.CreateAttribute('refinementLevel', Sdf.ValueTypeNames.Int).Set(2)


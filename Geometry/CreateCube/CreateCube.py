from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create cube.
pathName = '/World/cube'
cubeGeom = UsdGeom.Cube.Define(stage, pathName)

# Set cube size.
cubeGeom.CreateSizeAttr(10.0)

# Set color.
cubeGeom.CreateDisplayColorAttr([(0.0, 1.0, 0.0)])

# Set position.
UsdGeom.XformCommonAPI(cubeGeom).SetTranslate((0.0, 5.0, 0.0))

# Set scale.
UsdGeom.XformCommonAPI(cubeGeom).SetScale((2.0, 1.0, 2.0))

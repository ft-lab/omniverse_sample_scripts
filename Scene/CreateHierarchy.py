from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Get root path.
rootPath = ''
if defaultPrim.IsValid():
    rootPath = defaultPrim.GetPath().pathString

# Create empty node(Xform).
UsdGeom.Xform.Define(stage, rootPath + '/node1')

# Create empty node(Xform).
UsdGeom.Xform.Define(stage, rootPath + '/node1/node1_2')

# Create sphere.
pathName = rootPath + '/node1/sphere'
sphereGeom = UsdGeom.Sphere.Define(stage, pathName)

# Set radius.
sphereGeom.CreateRadiusAttr(1.0)

# Set position.
UsdGeom.XformCommonAPI(sphereGeom).SetTranslate((-3, 0, 0))

# Create cube.
pathName = rootPath + '/node1/cube'
cubeGeom = UsdGeom.Cube.Define(stage, pathName)

# Set position.
UsdGeom.XformCommonAPI(cubeGeom).SetTranslate((0, 0, 0))

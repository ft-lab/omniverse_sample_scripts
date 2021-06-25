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

# Set transform.
prim = stage.GetPrimAtPath(pathName)
prim.CreateAttribute("xformOp:translate", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(0, 10, 0))
prim.CreateAttribute("xformOp:scale", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(1, 2, 1))
prim.CreateAttribute("xformOp:rotateXYZ", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(120, 45, 0))

transformOrder = prim.CreateAttribute("xformOpOrder", Sdf.ValueTypeNames.String, False)
transformOrder.Set(["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"])

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Y-Up.
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

rootPath = '/World'

# Physics scene definition.
scene = UsdPhysics.Scene.Define(stage, rootPath + '/physicsScene')
scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
scene.CreateGravityMagnitudeAttr().Set(981.0)

hPos = 15.0

# --------------------------------------------.
# cube0.
# --------------------------------------------.
cube0Path = rootPath + '/cube0'
cube0Geom = UsdGeom.Cube.Define(stage, cube0Path)

# Set cube size.
cube0Geom.CreateSizeAttr(10.0)

# Set color.
cube0Geom.CreateDisplayColorAttr([(0.0, 1.0, 0.0)])

# Set position.
UsdGeom.XformCommonAPI(cube0Geom).SetTranslate((0.0, hPos, 0.0))

# Set scale.
UsdGeom.XformCommonAPI(cube0Geom).SetScale((2.0, 0.5, 0.5))

# --------------------------------------------.
# cube1.
# --------------------------------------------.
cube1Path = rootPath + '/cube1'
cube1Geom = UsdGeom.Cube.Define(stage, cube1Path)

# Set cube size.
cube1Geom.CreateSizeAttr(10.0)

# Set color.
cube1Geom.CreateDisplayColorAttr([(0.0, 0.0, 1.0)])

# Set position.
UsdGeom.XformCommonAPI(cube1Geom).SetTranslate((21.0, hPos, 0.0))

# Set scale.
UsdGeom.XformCommonAPI(cube1Geom).SetScale((2.0, 0.5, 0.5))

# --------------------------------------------.
# cube2.
# --------------------------------------------.
cube2Path = rootPath + '/cube2'
cube2Geom = UsdGeom.Cube.Define(stage, cube2Path)

# Set cube size.
cube2Geom.CreateSizeAttr(10.0)

# Set color.
cube2Geom.CreateDisplayColorAttr([(0.0, 1.0, 1.0)])

# Set position.
UsdGeom.XformCommonAPI(cube2Geom).SetTranslate((42.0, hPos, 0.0))

# Set scale.
UsdGeom.XformCommonAPI(cube2Geom).SetScale((2.0, 0.5, 0.5))

# --------------------------------------------.
# Physics settings.
# --------------------------------------------.
# cube0 : static body
cube0Prim = stage.GetPrimAtPath(cube0Path)
UsdPhysics.CollisionAPI.Apply(cube0Prim)

# cube1 : dynamic body
cube1Prim = stage.GetPrimAtPath(cube1Path)
UsdPhysics.CollisionAPI.Apply(cube1Prim)
UsdPhysics.RigidBodyAPI.Apply(cube1Prim)

# cube2 : dynamic body
cube2Prim = stage.GetPrimAtPath(cube2Path)
UsdPhysics.CollisionAPI.Apply(cube2Prim)
UsdPhysics.RigidBodyAPI.Apply(cube2Prim)

# ----------------------------------------.
# Setup joint.
# ----------------------------------------.
jointPath = rootPath + '/revoluteJoint'
revoluteJoint = UsdPhysics.RevoluteJoint.Define(stage, jointPath)

# define revolute joint axis and its limits, defined in degrees
revoluteJoint.CreateAxisAttr("Z")
revoluteJoint.CreateLowerLimitAttr(-50.0)
revoluteJoint.CreateUpperLimitAttr(50.0)

# define revolute joint bodies
revoluteJoint.CreateBody0Rel().SetTargets([cube0Path])
revoluteJoint.CreateBody1Rel().SetTargets([cube1Path])

# define revolute joint local poses for bodies
revoluteJoint.CreateLocalPos0Attr().Set(Gf.Vec3f(5.25, 0.0, 0.0))
revoluteJoint.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))

revoluteJoint.CreateLocalPos1Attr().Set(Gf.Vec3f(-5.25, 0.0, 0.0))
revoluteJoint.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))

# set break force/torque
revoluteJoint.CreateBreakForceAttr().Set(1e20)
revoluteJoint.CreateBreakTorqueAttr().Set(1e20)

# optionally add angular drive for example
angularDriveAPI = UsdPhysics.DriveAPI.Apply(stage.GetPrimAtPath(jointPath), "angular")
angularDriveAPI.CreateTypeAttr("force")
angularDriveAPI.CreateMaxForceAttr(100.0)
angularDriveAPI.CreateTargetVelocityAttr(1.0)
angularDriveAPI.CreateDampingAttr(100.0)
angularDriveAPI.CreateStiffnessAttr(0.0)

# ----------------------------------------.
# Setup joint2.
# ----------------------------------------.
jointPath2 = rootPath + '/revoluteJoint2'
revoluteJoint2 = UsdPhysics.RevoluteJoint.Define(stage, jointPath2)

# define revolute joint axis and its limits, defined in degrees
revoluteJoint2.CreateAxisAttr("Z")
revoluteJoint2.CreateLowerLimitAttr(-50.0)
revoluteJoint2.CreateUpperLimitAttr(50.0)

# define revolute joint bodies
revoluteJoint2.CreateBody0Rel().SetTargets([cube1Path])
revoluteJoint2.CreateBody1Rel().SetTargets([cube2Path])

# define revolute joint local poses for bodies
revoluteJoint2.CreateLocalPos0Attr().Set(Gf.Vec3f(5.25, 0.0, 0.0))
revoluteJoint2.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))

revoluteJoint2.CreateLocalPos1Attr().Set(Gf.Vec3f(-5.25, 0.0, 0.0))
revoluteJoint2.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))

# set break force/torque
revoluteJoint2.CreateBreakForceAttr().Set(1e20)
revoluteJoint2.CreateBreakTorqueAttr().Set(1e20)

# optionally add angular drive for example
#angularDriveAPI2 = UsdPhysics.DriveAPI.Apply(stage.GetPrimAtPath(jointPath2), "angular")
#angularDriveAPI2.CreateTypeAttr("force")
#angularDriveAPI2.CreateMaxForceAttr(100.0)
#angularDriveAPI2.CreateTargetVelocityAttr(1.0)
#angularDriveAPI2.CreateDampingAttr(100.0)
#angularDriveAPI2.CreateStiffnessAttr(0.0)

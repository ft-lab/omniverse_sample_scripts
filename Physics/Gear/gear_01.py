from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf, UsdSkel, PhysxSchema
import math

# gear path.
gear_basePath = '/World/gears'

# Get stage.
g_stage = omni.usd.get_context().get_stage()

# Y-Up.
UsdGeom.SetStageUpAxis(g_stage, UsdGeom.Tokens.y)

xformCache = UsdGeom.XformCache(0)

# ------------------------------------------
# Get prim center position.
# @param[in] primPath   Prim path.
# @return  position(Gf.Vec3f)
# ------------------------------------------
def GetPrimCenter (primPath : str):
    prim = g_stage.GetPrimAtPath(primPath)
    if prim.IsValid() == False:
        return
    
    globalPose = xformCache.GetLocalToWorldTransform(prim)
    translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

    return translate

# ------------------------------------------
# Set RigidBody on gear.
# ------------------------------------------
def SetRigidBodyOnGear (primPath : str, index : int):
    prim = g_stage.GetPrimAtPath(primPath)
    if prim.IsValid() == False:
        return

    physicsAPI = UsdPhysics.RigidBodyAPI.Apply(prim)
    UsdPhysics.MassAPI.Apply(prim)

    UsdPhysics.CollisionAPI.Apply(prim)

    pos = GetPrimCenter(primPath)

    # revolute joint
    path = gear_basePath + '/revoluteJoint_' + str(index)
    revoluteJoint = UsdPhysics.RevoluteJoint.Define(g_stage, path)
    revoluteJoint.CreateAxisAttr("Z")
    revoluteJoint.CreateBody1Rel().SetTargets([primPath])
    revoluteJoint.CreateLocalPos0Attr().Set(pos)        
    revoluteJoint.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))

    revoluteJoint.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
    revoluteJoint.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))

# -----------------------------------------------
# gear1 path.
gear1_path = gear_basePath + '/gear'

# gear2 path.
gear2_path = gear_basePath + '/gear_1'

# gear3 path.
gear3_path = gear_basePath + '/gear_2'

# Radius.
radius1 = 5.0
radius2 = 10.0
radius3 = 6.25

# Physics scene definition.
scene = UsdPhysics.Scene.Define(g_stage, "/physicsScene")
scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
scene.CreateGravityMagnitudeAttr().Set(981.0)

gear1_prim = g_stage.GetPrimAtPath(gear1_path)

pos1 = GetPrimCenter(gear1_path)

# Set RigidBody on gear.
SetRigidBodyOnGear(gear1_path, 0)
SetRigidBodyOnGear(gear2_path, 1)
SetRigidBodyOnGear(gear3_path, 2)

# add angular drive.
revolute0_path = gear_basePath + "/revoluteJoint_0"
revolute1_path = gear_basePath + "/revoluteJoint_1"
revolute2_path = gear_basePath + "/revoluteJoint_2"

#angularDriveAPI = UsdPhysics.DriveAPI.Apply(g_stage.GetPrimAtPath(revolute0_path), "angular")
#angularDriveAPI.CreateTypeAttr("force")        
#angularDriveAPI.CreateMaxForceAttr(1e20)
#angularDriveAPI.CreateTargetVelocityAttr(45.0)
#angularDriveAPI.CreateTargetPositionAttr(0.0)
#angularDriveAPI.CreateDampingAttr(1e10)
#angularDriveAPI.CreateStiffnessAttr(0.0)

# gear joint (0-1)
gearJoint = PhysxSchema.PhysxPhysicsGearJoint.Define(g_stage, "/gearJoint_0_1")

gearJoint.CreateBody0Rel().SetTargets([gear1_path])
gearJoint.CreateBody1Rel().SetTargets([gear2_path])

gearJoint.CreateGearRatioAttr(radius1/radius2)
gearJoint.CreateHinge0Rel().SetTargets([revolute0_path])
gearJoint.CreateHinge1Rel().SetTargets([revolute1_path])

# gear joint (0-2)
gearJoint2 = PhysxSchema.PhysxPhysicsGearJoint.Define(g_stage, "/gearJoint_0_2")

gearJoint2.CreateBody0Rel().SetTargets([gear1_path])
gearJoint2.CreateBody1Rel().SetTargets([gear3_path])

gearJoint2.CreateGearRatioAttr(radius1/radius3)
gearJoint2.CreateHinge0Rel().SetTargets([revolute0_path])
gearJoint2.CreateHinge1Rel().SetTargets([revolute2_path])

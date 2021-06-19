from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import math
import random

# Get stage.
g_stage = omni.usd.get_context().get_stage()

# Y-Up.
UsdGeom.SetStageUpAxis(g_stage, UsdGeom.Tokens.y)

# Physics scene definition.
scene = UsdPhysics.Scene.Define(g_stage, "/physicsScene")
scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
scene.CreateGravityMagnitudeAttr().Set(981.0)

# Create Xform.
g_basePath = '/World/spheres'
xformPrim = UsdGeom.Xform.Define(g_stage, g_basePath)

# --------------------------------------------------------.
# Create sphere.
# @param[in] index    serial number.
# @param[in] radius   radius of sphere.
# @param[in] wPos     world position (x, y, z).
# @param[in] colorV   color (red, green, blue).
# --------------------------------------------------------.
def createSphere(index, radius, wPos, colorV):

    # Create sphere.
    name = 'sphere_' + str(index)
    path = g_basePath + '/' + name
    spherePrim = UsdGeom.Sphere.Define(g_stage, path)

    # Set radius.
    spherePrim.CreateRadiusAttr(radius)

    # Set color.
    spherePrim.CreateDisplayColorAttr([colorV])

    objPrim = g_stage.GetPrimAtPath(path)

    # Set position.
    UsdGeom.XformCommonAPI(spherePrim).SetTranslate(wPos)

    # Create collider.
    UsdPhysics.CollisionAPI.Apply(objPrim)

    # Rigid body.
    rigidBodyAPI = UsdPhysics.RigidBodyAPI.Apply(objPrim)

# -----------------------------------------------------------.
# -----------------------------------------------------------.

r = 100.0
sR = 10.0
rCount = 32

fV = 0.0
fVD = 2.0 * math.pi / (float)(rCount)
fy = 50.0
fyD = 1.0
for i in range(200):
    fx = r * math.cos(fV)
    fz = r * math.sin(fV)

    colR = random.random()
    colG = random.random()
    colB = random.random()

    createSphere(i, sR, (fx, fy, fz), (colR, colG, colB))

    fV += fVD
    fy += fyD

    if (i & 15) == 15:
        r *= 0.9
        sR *= 0.9
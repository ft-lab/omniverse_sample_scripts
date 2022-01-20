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
# Create ground.
# --------------------------------------------------------.
def createGround ():
    # Create cube.
    path = '/World/ground'
    cubeGeom = UsdGeom.Cube.Define(g_stage, path)

    # Set color.
    cubeGeom.CreateDisplayColorAttr([(0.2, 0.2, 0.2)])

    # Set position.
    UsdGeom.XformCommonAPI(cubeGeom).SetTranslate((0.0, -5.0, 0.0))

    # Set scale.
    UsdGeom.XformCommonAPI(cubeGeom).SetScale((200.0, 10, 200.0))

    # Create collider.
    objPrim = g_stage.GetPrimAtPath(path)
    UsdPhysics.CollisionAPI.Apply(objPrim)

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
    UsdPhysics.MeshCollisionAPI(objPrim).CreateApproximationAttr("boundingSphere")
    UsdPhysics.MeshCollisionAPI.Apply(objPrim)

    # Rigid body.
    rigidBodyAPI = UsdPhysics.RigidBodyAPI.Apply(objPrim)

# --------------------------------------------------------.
# Create cube.
# @param[in] wPos     world position (x, y, z).
# @param[in] wSize    size (x, y, z).
# --------------------------------------------------------.
def createCube (index, wPos, wSize):
    name = 'cube_' + str(index)
    path = '/World/' + name
    cubePrim = UsdGeom.Cube.Define(g_stage, path)

    # Set cube size.
    cubePrim.CreateSizeAttr(1.0)

    # Set color.
    cubePrim.CreateDisplayColorAttr([(0.2, 0.2, 0.2)])

    # Set position.
    UsdGeom.XformCommonAPI(cubePrim).SetTranslate((wPos[0], wPos[1], wPos[2]))

    # Set scale.
    UsdGeom.XformCommonAPI(cubePrim).SetScale((wSize[0], wSize[1], wSize[2]))

    # Create collider.
    objPrim = g_stage.GetPrimAtPath(path)
    UsdPhysics.CollisionAPI.Apply(objPrim)

# --------------------------------------------------------.
# Create wall.
# --------------------------------------------------------.
def createWall ():
    createCube(0, [-200.0, 25.0,    0.0], [ 10.0, 50.0, 400.0])
    createCube(1, [ 200.0, 25.0,    0.0], [ 10.0, 50.0, 400.0])
    createCube(2, [   0.0, 25.0, -200.0], [400.0, 50.0,  10.0])
    createCube(3, [   0.0, 25.0,  200.0], [400.0, 50.0,  10.0])

# -----------------------------------------------------------.
# -----------------------------------------------------------.

# Create ground.
createGround()

# Create wall.
createWall()

# Create spheres.
sR = 5.0
dd = 15.0
sCount = 16
dMin = dd * (float)(sCount) * 0.5

i = 0
fy = 30.0
for y in range(10):
    fz = -dMin
    for z in range(sCount):
        fx = -dMin
        for x in range(sCount):
            colR = random.random()
            colG = random.random()
            colB = random.random()
            dx = random.random() * 5.0
            dz = random.random() * 5.0

            createSphere(i, sR, (fx + dx, fy, fz + dz), (colR, colG, colB))
            i = i + 1
            fx += dd
        fz += dd
    fy += dd



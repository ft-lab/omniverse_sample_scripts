from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import random
import omni.physx

# Get stage.
stage = omni.usd.get_context().get_stage()

# Y-Up.
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString

# Physics scene definition.
scene = UsdPhysics.Scene.Define(stage, defaultPrimPath + '/physicsScene')
scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
scene.CreateGravityMagnitudeAttr().Set(981.0)

# --------------------------------------------.
# Create cube.
# --------------------------------------------.
def CreateCube (name : str, pos : Gf.Vec3f, scale : Gf.Vec3f):
    path = defaultPrimPath + '/cubes'
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        UsdGeom.Xform.Define(stage, path)

    cubePath = path + '/' + name
    cubeGeom = UsdGeom.Cube.Define(stage, cubePath)

    # Set cube size.
    cubeGeom.CreateSizeAttr(10.0)

    # Set color.
    cubeGeom.CreateDisplayColorAttr([(0.0, 1.0, 0.0)])

    # Set position.
    UsdGeom.XformCommonAPI(cubeGeom).SetTranslate((pos[0], pos[1], pos[2]))

    # Set scale.
    UsdGeom.XformCommonAPI(cubeGeom).SetScale((scale[0], scale[1], scale[2]))

    # Physics settings.
    cubePrim = stage.GetPrimAtPath(cubePath)
    UsdPhysics.CollisionAPI.Apply(cubePrim)

# --------------------------------------------.
# Create red sphere.
# --------------------------------------------.
def CreateRedSphere (name : str, pos : Gf.Vec3f, radius : float):
    path = defaultPrimPath + '/spheres'
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        UsdGeom.Xform.Define(stage, path)

    spherePath = path + '/' + name
    sphereGeom = UsdGeom.Sphere.Define(stage, spherePath)

    # Set radius.
    sphereGeom.CreateRadiusAttr(radius)

    # Set color.
    sphereGeom.CreateDisplayColorAttr([(1.0, 0.0, 0.0)])

    # Set position.
    UsdGeom.XformCommonAPI(sphereGeom).SetTranslate((pos[0], pos[1], pos[2]))

# ------------------------------------------------------.
# Create cubes.
areaV = 100.0
cubeScale = 1.0

for i in range(50):
    posX = (random.random() - 0.5) * areaV 
    posY = (random.random() - 0.5) * (areaV * 0.1)
    posZ = (random.random() - 0.5) * areaV + 100.0

    pos   = Gf.Vec3f(posX, posY, posZ)
    scale = Gf.Vec3f(cubeScale, cubeScale, cubeScale)
    name = 'cube_' + str(i)
    CreateCube(name, pos, scale)

# Remove spheres.
path = defaultPrimPath + '/spheres'
prim = stage.GetPrimAtPath(path)
if prim.IsValid():
    stage.RemovePrim(path)

# Callback for Rayhit.
# rayhit works during animation playback.
sphereIndex = 0
def ray_hit (hit):
    global sphereIndex
    print("distance : " + str(hit.distance))
    print("Hit position : " + str(hit.position))
    print("Hit normal : " + str(hit.normal))
    print("Collision prim path : " + str(hit.collision))

    # Get collision prim.
    prim = stage.GetPrimAtPath(hit.collision)
    print("   name : " + str(prim.GetName()))
    print("-----------------------------")

    # Create sphere.
    name = "sphere_" + str(sphereIndex)
    CreateRedSphere(name, hit.position, 1.0)
    sphereIndex += 1

for i in range(100):
    # Ray position.
    rayPos = Gf.Vec3f(0, 0, 0)

    # Ray direction.
    dx = (random.random() - 0.5) * 0.3
    dy = (random.random() - 0.5) * 0.3
    dz = 1.0
    rayDir = Gf.Vec3f(dx, dy, dz).GetNormalized()

    # Ray distance.
    distance = 10000.0

    # raycast.
    omni.physx.get_physx_scene_query_interface().raycast_all(rayPos, rayDir, distance, ray_hit)


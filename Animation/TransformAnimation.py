from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create sphere.
def createSphere(primPath : str, radius : float = 10.0, pos : Gf.Vec3f = Gf.Vec3f(0, 0, 0)):
    # Create sphere.
    sphereGeom = UsdGeom.Sphere.Define(stage, primPath)

    # Set radius.
    sphereGeom.CreateRadiusAttr(radius)

    # Set color.
    sphereGeom.CreateDisplayColorAttr([(1.0, 0.0, 0.0)])

    # Set position.
    UsdGeom.XformCommonAPI(sphereGeom).SetTranslate(Gf.Vec3d(pos))

    # Set refinement.
    objPrim = stage.GetPrimAtPath(primPath)
    objPrim.CreateAttribute('refinementEnableOverride', Sdf.ValueTypeNames.Bool).Set(True)
    objPrim.CreateAttribute('refinementLevel', Sdf.ValueTypeNames.Int).Set(2)

    return objPrim

primPath = "/World/sphere"
prim = createSphere(primPath, 20.0)

# Set Keyframe.
xformAPI = UsdGeom.XformCommonAPI(prim)
xformAPI.SetTranslate(Gf.Vec3d(0, 0, 0), Usd.TimeCode(0))
xformAPI.SetTranslate(Gf.Vec3d(0, 100, 0), Usd.TimeCode(50))
xformAPI.SetTranslate(Gf.Vec3d(200, 100, 0), Usd.TimeCode(100))

rotationOrder = UsdGeom.XformCommonAPI.RotationOrderXYZ
xformAPI.SetRotate(Gf.Vec3f(0, 0, 0), rotationOrder, Usd.TimeCode(0))
xformAPI.SetRotate(Gf.Vec3f(30, 0, 0), rotationOrder, Usd.TimeCode(50))
xformAPI.SetRotate(Gf.Vec3f(30, 0, 50), rotationOrder, Usd.TimeCode(100))

xformAPI.SetScale(Gf.Vec3f(1, 2, 1), Usd.TimeCode(0))
xformAPI.SetScale(Gf.Vec3f(1, 2, 1), Usd.TimeCode(50))
xformAPI.SetScale(Gf.Vec3f(1, 2, 1), Usd.TimeCode(100))


# Clear cache.
xformCache = UsdGeom.XformCache()
xformCache.Clear()

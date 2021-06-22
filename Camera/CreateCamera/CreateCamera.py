from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create camera.
pathName = '/World/camera'
cameraGeom = UsdGeom.Camera.Define(stage, pathName)

cameraGeom.CreateFocalLengthAttr(24.0)
cameraGeom.CreateFocusDistanceAttr(400.0)
cameraGeom.CreateFStopAttr(0.0)
cameraGeom.CreateProjectionAttr('perspective')

# Set position.
UsdGeom.XformCommonAPI(cameraGeom).SetTranslate((0.0, 20.0, 40.0))

# Set rotation.
UsdGeom.XformCommonAPI(cameraGeom).SetRotate((-20, 15.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

# Change active camera.
viewport = omni.kit.viewport.get_viewport_interface()
viewport.get_viewport_window().set_active_camera(pathName)

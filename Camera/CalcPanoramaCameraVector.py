from pxr import Usd, UsdGeom, CameraUtil, UsdShade, Sdf, Gf, Tf
import omni.kit

# IPD (cm).
ipdValue = 6.4

# Get viewport.
# Kit103 : changed from omni.kit.viewport to omni.kit.viewport_legacy
#viewport = omni.kit.viewport_legacy.get_viewport_interface()
#viewportWindow = viewport.get_viewport_window()

# Kit104 : changed from omni.kit.viewport_legacy to omni.kit.viewport.utility.get_active_viewport_window
import omni.kit.viewport.utility

# Get active viewport window.
active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api

# Get camera path ("/OmniverseKit_Persp" etc).
cameraPath = viewport_api.camera_path.pathString

# Get stage.
stage = omni.usd.get_context().get_stage()

#time_code = omni.timeline.get_timeline_interface().get_current_time() * stage.GetTimeCodesPerSecond()
time_code = Usd.TimeCode.Default()

# ---------------------------------.
# Create new camera.
# ---------------------------------.
def createNewCamera (orgCamera : Gf.Camera, pathName : str, position : Gf.Vec3f, direction : Gf.Vec3f):
    cameraGeom = UsdGeom.Camera.Define(stage, pathName)

    cameraGeom.CreateFocusDistanceAttr(orgCamera.GetFocusDistanceAttr().Get())
    cameraGeom.CreateFocalLengthAttr(orgCamera.GetFocalLengthAttr().Get())
    cameraGeom.CreateFStopAttr(orgCamera.GetFStopAttr().Get())

    # Set position.
    UsdGeom.XformCommonAPI(cameraGeom).SetTranslate((position[0], position[1], position[2]))

    # Set rotation(Y-Up (0, 1, 0)).
    m = Gf.Matrix4f().SetLookAt(Gf.Vec3f(0, 0, 0), direction, Gf.Vec3f(0, 1, 0))
    rV = -m.ExtractRotation().Decompose(Gf.Vec3d(1, 0, 0), Gf.Vec3d(0, 1, 0), Gf.Vec3d(0, 0, 1))
    UsdGeom.XformCommonAPI(cameraGeom).SetRotate((rV[0], rV[1], rV[2]), UsdGeom.XformCommonAPI.RotationOrderXYZ)

    # Set scale.
    UsdGeom.XformCommonAPI(cameraGeom).SetScale((1, 1, 1))

# ---------------------------------.
# Get active camera.
cameraPrim = stage.GetPrimAtPath(cameraPath)
if cameraPrim.IsValid():
    camera  = UsdGeom.Camera(cameraPrim)    # UsdGeom.Camera
    cameraV = camera.GetCamera(time_code)   # Gf.Camera

    # Get view matrix.
    viewMatrix = cameraV.frustum.ComputeViewMatrix()

    # Two camera positions in the view.
    ipdH = ipdValue * 0.5
    leftVPos  = Gf.Vec3f(-ipdH, 0, 0)
    rightVPos = Gf.Vec3f( ipdH, 0, 0)

    # Camera vector(World).
    viewInv = viewMatrix.GetInverse()
    vVector = viewInv.TransformDir(Gf.Vec3f(0, 0, -1))

    # Convert to camera position in world coordinates.
    leftWPos  = viewInv.Transform(leftVPos)
    rightWPos = viewInv.Transform(rightVPos)

    # Create camera.
    pathStr = '/World'
    leftPathStr = pathStr + '/camera_left'
    createNewCamera(camera, leftPathStr, leftWPos, vVector)

    rightPathStr = pathStr + '/camera_right'
    createNewCamera(camera, rightPathStr, rightWPos, vVector)
    



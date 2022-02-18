from pxr import Usd, UsdGeom, UsdPhysics, UsdSkel, UsdShade, Sdf, Gf, Tf

import omni.ui
import omni.kit.app
import carb.events
import asyncio

# Get main window viewport.
window = omni.ui.Window('Viewport')
viewportI = omni.kit.viewport.acquire_viewport_interface()
vWindow = viewportI.get_viewport_window(None)

viewportRect = None
viewportSize = None
cameraAspect = 0.0
viewportUIOriginPos = None

# Get stage.
stage = omni.usd.get_context().get_stage()

time_code = omni.timeline.get_timeline_interface().get_current_time() * stage.GetTimeCodesPerSecond()

# ------------------------------------------.
# Get Screen position(rendering) to viewport position(pixel).
# ------------------------------------------.
def getScreenToViewportPos (screenPos):
    global viewportSize
    global cameraAspect
    global viewportUIOriginPos

    aspect = viewportSize[0] / viewportSize[1]

    sx = viewportSize[0] * 0.5 * (1.0 + screenPos[0])
    sy = viewportSize[1] * 0.5 * (1.0 - screenPos[1] / (cameraAspect / aspect))

    rPos = Gf.Vec2f(sx + viewportUIOriginPos[0], sy + viewportUIOriginPos[1])

    return rPos

# ------------------------------------------.
# Show the name of the selected Prim.
# ------------------------------------------.
def ShowNameOfSelectedPrim ():
    global viewportRect
    global viewportSize
    global cameraAspect
    global viewportUIOriginPos

    # Get active camera.
    aCamera = vWindow.get_active_camera()
    cameraPrim = stage.GetPrimAtPath(aCamera)
    if cameraPrim.IsValid() == False:
        return

    # Get camera matrix.
    camera = UsdGeom.Camera(cameraPrim)         # Geom.Camera
    cameraV = camera.GetCamera(time_code)       # Gf.Camera
    frustum = cameraV.frustum
    viewMatrix       = frustum.ComputeViewMatrix()
    projectionMatrix = frustum.ComputeProjectionMatrix()

    # AspectRatio.
    cameraAspect = cameraV.aspectRatio

    # Get selection.
    selection = omni.usd.get_context().get_selection()
    paths = selection.get_selected_prim_paths()

    # Get viewport rect.
    viewportRect = vWindow.get_viewport_rect()
    viewportSize = (viewportRect[2] - viewportRect[0], viewportRect[3] - viewportRect[1])

    captionHeight = 24  # Height of the caption in the Viewport window.
    margin = 2          # frame size.

    # Get Viewport window (UI).
    uiViewportWindow = omni.ui.Workspace.get_window("Viewport")

    # Calculate the origin of the viewport as UI.
    mX = (uiViewportWindow.width - margin * 2.0  - viewportSize[0]) * 0.5
    mY = (uiViewportWindow.height - margin * 2.0 - captionHeight - viewportSize[1]) * 0.5
    viewportUIOriginPos = (mX, mY)

    sPosList = []
    nameList = []

    xformCache = UsdGeom.XformCache(0)

    for path in paths:
        prim = stage.GetPrimAtPath(path)
        if prim.GetTypeName() == "Xform" or prim.GetTypeName() == "Mesh":
            # Get world Transform.
            globalPose = xformCache.GetLocalToWorldTransform(prim)

            # Decompose transform.
            translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)
            wTargetPos = Gf.Vec3d(translate[0], translate[1], translate[2])

            # Get ray from world space position.
            rayV = frustum.ComputePickRay(wTargetPos)

            # ray.direction to screen pos.
            vPos = viewMatrix.Transform(wTargetPos)

            # screen position : -1.0 to +1.0
            # Depending on the aspect ratio, the value may be greater than 1.0.
            sPos = projectionMatrix.Transform(vPos)     
            
            # Convert screen position to viewport position.
            sViewportPos = getScreenToViewportPos(sPos)

            sPosList.append(sViewportPos)
            nameList.append(prim.GetName())

    if len(sPosList) > 0:
        with window.frame:
            with omni.ui.ZStack():
                for i in range(len(sPosList)):
                    with omni.ui.VStack(height=0):
                        with omni.ui.Placer(offset_x=sPosList[i][0], offset_y=sPosList[i][1]):
                            f = omni.ui.Label(nameList[i])
                            f.set_style({"color": 0xffc0ffff, "font_size": 20})
 

# ------------------------------------------.
# Update event.
# ------------------------------------------.
def on_update(e: carb.events.IEvent):
    ShowNameOfSelectedPrim()

# ------------------------------------------.
# Register for update events.
# To clear the event, specify "subs=None".
subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update, name="Draw prim name update")

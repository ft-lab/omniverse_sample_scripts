from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import asyncio
from PIL import Image
import ctypes
import carb

from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_buffer, create_viewport_window, get_viewport_from_window_name
from omni.kit.viewport.utility.camera_state import ViewportCameraState

# See also : https://forums.developer.nvidia.com/t/how-to-get-the-backbuffer-of-omniverses-current-viewport/236825

# -------------------------------------------.
# Search for viewport with specified name.
# -------------------------------------------.
def SearchViewportWindow(window_name : str):
    try:
        from omni.kit.viewport.window import get_viewport_window_instances
        for window in get_viewport_window_instances(None):
            if window.title == window_name:
                return window
    except ImportError:
        pass
    return None

# -------------------------------------------.
# Capture LDR.
# -------------------------------------------.
async def captureCamera(cameraPrimPath : str):
    if cameraPrimPath == None or cameraPrimPath == "":
        carb.log_error("Camera path is not specified.")
        return

    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath(cameraPrimPath)
    if prim.IsValid() == False:
        carb.log_error(f"[{cameraPrimPath}] could not be found.")
        return

    # Create a Viewport corresponding to the camera.
    # If a Viewport already exists, reuse it.
    viewportName = "Viewport Camera"

    #viewport_api = get_viewport_from_window_name(viewportName)
    viewport_api = None
    viewportWindow = SearchViewportWindow(viewportName)
    if viewportWindow != None:
        viewport_api = viewportWindow.viewport_api

    if viewport_api == None:
        # Create new viewport.
        viewportWindow = create_viewport_window(viewportName, width=800, height=600)
        viewport_api = viewportWindow.viewport_api

    # Hide Viewport
    viewportWindow.visible = False

    if viewport_api == None:
        carb.log_error("Viewport could not be created.")
        return

    viewport_api.set_active_camera(cameraPrimPath)
    await viewport_api.wait_for_rendered_frames()

    # Called when capture is complete.
    cImage = None
    callbackExit = False
    def capture_callback(buffer, buffer_size, width, height, format):
        nonlocal cImage
        nonlocal callbackExit

        print(f"Buffer size : {buffer_size}")
        print(f"Resolution : {width} x {height} ")
        print(f"TextureFormat : {format}")  # TextureFormat.RGBA8_UNORM

        if str(format) != "TextureFormat.RGBA8_UNORM":
            callbackExit = True
            return

        # Get capture image.
        try:
            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.POINTER(ctypes.c_byte * buffer_size)
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
            content = ctypes.pythonapi.PyCapsule_GetPointer(buffer, None)
        except Exception as e:
            carb.log_error(f"Failed to get capture buffer: {e}")
            callbackExit = True
            return

        # Create image.
        # content.contents is RGBA buffers.
        cImage = Image.frombytes("RGBA", (width, height), content.contents)

        callbackExit = True

    # Capturing.
    cap_obj = capture_viewport_to_buffer(viewport_api, capture_callback)
    await omni.kit.app.get_app_interface().next_update_async()

    # Wait for a callback to return from a callback.
    while callbackExit == False:
        await asyncio.sleep(0.05)

    # Destroy Viewport window.
    # Note that Viewport must be discarded completely or it will consume the GPU.
    viewportWindow.destroy()
    viewportWindow = None

    print(f"Capture complete.")

    # Show image.
    if cImage != None:
        cImage.show()

# -------------------------------------------.

asyncio.ensure_future( captureCamera("/World/Camera") )



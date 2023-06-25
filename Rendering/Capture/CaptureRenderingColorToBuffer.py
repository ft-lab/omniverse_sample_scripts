from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import asyncio
from PIL import Image
import ctypes
import carb

from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_buffer

# See also : https://forums.developer.nvidia.com/t/how-to-get-the-backbuffer-of-omniverses-current-viewport/236825

# -------------------------------------------.
# Capture LDR.
# -------------------------------------------.
async def capture():
    # Get active viewport.
    active_viewport = get_active_viewport()

    await active_viewport.wait_for_rendered_frames()

    # Called when capture is complete.
    callbackExit = False
    def capture_callback(buffer, buffer_size, width, height, format):
        nonlocal callbackExit
        print(f"Buffer size : {buffer_size}")
        print(f"Resolution : {width} x {height} ")
        print(f"TextureFormat : {format}")  # TextureFormat.RGBA8_UNORM

        # Get capture image.
        if str(format) == "TextureFormat.RGBA8_UNORM":
            # Get buffer from void *.
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
            image = Image.frombytes("RGBA", (width, height), content.contents)

            # Show.
            image.show()

            callbackExit = True

    # Capturing.
    cap_obj = capture_viewport_to_buffer(active_viewport, capture_callback)
    await omni.kit.app.get_app_interface().next_update_async()

    # Wait for a callback to return from a callback.
    while callbackExit == False:
        await asyncio.sleep(0.05)

    print(f"Capture complete.")

# -------------------------------------------.
asyncio.ensure_future( capture() )



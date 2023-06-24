from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import asyncio
from PIL import Image
import ctypes

from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_buffer

# Referred to https://forums.developer.nvidia.com/t/how-to-get-the-backbuffer-of-omniverses-current-viewport/236825

# -------------------------------------------.
# Capture LDR.
# -------------------------------------------.
async def capture():
    # Get active viewport.
    active_viewport = get_active_viewport()

    await active_viewport.wait_for_rendered_frames()

    # Called when capture is complete.
    def capture_callback(buffer, buffer_size, width, height, format):
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
                return

            # Create image.
            # content.contents is RGBA buffers.
            image = Image.frombytes("RGBA", (width, height), content.contents)

            # Show.
            image.show()

    # Capturing.
    cap_obj = capture_viewport_to_buffer(active_viewport, capture_callback)
    await omni.kit.app.get_app_interface().next_update_async()

    # awaiting completion.
    result = await cap_obj.wait_for_result(completion_frames=30)

    print(f"Capture complete.")

# -------------------------------------------.
asyncio.ensure_future( capture() )



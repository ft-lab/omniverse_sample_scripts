from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import asyncio
import carb
import carb.settings

from omni.kit.viewport.utility import get_active_viewport, capture_viewport_to_file

# Referred to omni.kit.capture.

# -------------------------------------------.
# Capture LDR/HDR.
# -------------------------------------------.
async def capture(filePath : str, hdr : bool = False):
    # Assign ldr/hdr in settings.
    settings = carb.settings.get_settings()
    prevAsyncRendering = settings.get("/app/asyncRendering")
    prevAsyncRenderingLowLatency = settings.get("/app/asyncRenderingLowLatency")
    prevHdr = settings.get("/app/captureFrame/hdr")

    settings.set("/app/asyncRendering", False)
    settings.set("/app/asyncRenderingLowLatency", False)
    settings.set("/app/captureFrame/hdr", hdr)

    # Get active viewport.
    active_viewport = get_active_viewport()

    await active_viewport.wait_for_rendered_frames()

    # Capturing.
    cap_obj = capture_viewport_to_file(active_viewport, filePath, hdr)
    await omni.kit.app.get_app_interface().next_update_async()

    # awaiting completion.
    result = await cap_obj.wait_for_result(completion_frames=30)

    settings.set("/app/asyncRendering", prevAsyncRendering)
    settings.set("/app/asyncRenderingLowLatency", prevAsyncRenderingLowLatency)
    settings.set("/app/captureFrame/hdr", prevHdr)

    print(f"Capture complete [{filePath}].")

# -------------------------------------------.
asyncio.ensure_future( capture("K:/temp/output.png") )

# HDR capture not working?
asyncio.ensure_future( capture("K:/temp/output.exr", True) )


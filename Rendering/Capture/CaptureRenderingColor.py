from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.ui
import omni.kit.app

# Get main window viewport.
window = omni.ui.Window('Viewport')
viewportI = omni.kit.viewport_legacy.acquire_viewport_interface()
vWindow = viewportI.get_viewport_window(None)

# Get viewport image.
viewport_ldr = vWindow.get_drawable_ldr_resource()

# Save the Viewport image as a file.
# The path should be rewritten to match your environment.
filePath = "K:/temp/output.png"
renderer = omni.renderer_capture.acquire_renderer_capture_interface()
renderer.capture_next_frame_rp_resource(filePath, viewport_ldr)


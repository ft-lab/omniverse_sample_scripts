from pxr import Usd, UsdGeom, UsdPhysics, UsdSkel, UsdShade, Sdf, Gf, Tf
import omni.ui

# Get main window viewport.
viewportI = omni.kit.viewport.acquire_viewport_interface()
vWindow = viewportI.get_viewport_window(None)

# Get viewport rect.
viewportRect = vWindow.get_viewport_rect()
viewportSize = (viewportRect[2] - viewportRect[0], viewportRect[3] - viewportRect[1])
print(viewportRect)
print(viewportSize)


from pxr import Usd, UsdGeom, CameraUtil, UsdShade, Sdf, Gf, Tf
import omni.ext
import omni.ui
from omni.ui import color as cl
from omni.ui import scene as sc
import omni.kit

# Kit104 : Get active viewport window.
active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
viewport_api = active_vp_window.viewport_api

# World to NDC space (X : -1.0 to +1.0, Y : -1.0 to +1.0).
p = (0, 0, 0)
p_screen = viewport_api.world_to_ndc.Transform(p)

# NDC to Pixel space.
sPos, in_viewport = viewport_api.map_ndc_to_texture_pixel(p_screen)
if in_viewport:
    print(sPos)


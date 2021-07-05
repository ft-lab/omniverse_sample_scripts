from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import carb.settings

# Get rendering size.
# If Render Resolution is "Viewport", -1 will be set.
settings = carb.settings.get_settings()
width  = settings.get('/app/renderer/resolution/width')
height = settings.get('/app/renderer/resolution/height')

print("Rendering size : " + str(width) + " x " + str(height))

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import carb.settings

# Get Omniverse Kit version.
settings = carb.settings.get_settings()
kitVersion = settings.get('/crashreporter/data/buildVersion')

print("Kit Version : " + str(kitVersion))

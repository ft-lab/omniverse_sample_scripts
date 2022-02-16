from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
import omni.kit

# Change Post Processing parameter.
omni.kit.commands.execute("ChangeSetting", path="rtx/post/lensFlares/enabled", value=True)
omni.kit.commands.execute("ChangeSetting", path="rtx/post/lensFlares/flareScale", value=0.2)

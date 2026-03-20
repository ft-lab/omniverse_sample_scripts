from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd

# Get selection.
selection = omni.usd.get_context().get_selection()

pathStr = "/World"
selectedF = selection.is_prim_path_selected(pathStr)
if selectedF:
    print(f"[ {pathStr} ] Selected")
else:
    print(f"[ {pathStr} ] Not selected")


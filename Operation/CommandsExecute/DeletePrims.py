from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
selectedPaths = selection.get_selected_prim_paths()

# Delete prims.
omni.kit.commands.execute("DeletePrims", paths=selectedPaths)

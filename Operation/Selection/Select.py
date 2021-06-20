from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get selection.
selection = omni.usd.get_context().get_selection()

# Select one.
selection.set_selected_prim_paths(['/World'], True)

# Multiple selection.
selection.set_selected_prim_paths(['/World', '/World/defaultLight'], True)

# Deselection.
selection.clear_selected_prim_paths()

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
selectedPaths = selection.get_selected_prim_paths()

for path in selectedPaths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue

    newPathName = path + "_rename"

    # Rename Prim name.
    omni.kit.commands.execute("MovePrim", path_from=path, path_to=newPathName)
    break

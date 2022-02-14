from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Create empty node(Xform).
defaultPrimPath = defaultPrim.GetPath().pathString
xformPath = defaultPrimPath + '/Xform'
UsdGeom.Xform.Define(stage, xformPath)

# Get selection.
selection = omni.usd.get_context().get_selection()
selectedPaths = selection.get_selected_prim_paths()

for path in selectedPaths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue

    pathTo = xformPath + "/" + str(prim.GetName())

    # Change Prim's path.
    # path_from : Path of the original Prim.
    # path_to   : Path to move to.
    omni.kit.commands.execute("MovePrim", path_from=path, path_to=pathTo)



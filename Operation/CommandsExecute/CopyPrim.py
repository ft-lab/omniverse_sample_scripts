from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# Store select path.
pathList = []
for path in paths:
    pathList.append(path)

newPrimPathList = []
for path in pathList:
    # Duplicate Prim from specified path.
    omni.kit.commands.execute("CopyPrim", path_from=path)

    # Stores the path of the newly duplicated Prim.
    selection = omni.usd.get_context().get_selection()
    paths = selection.get_selected_prim_paths()
    if len(paths) >= 1:
        newPrimPathList.append(paths[0])

# Show the path of the newly duplicated Prim.
print(newPrimPathList)

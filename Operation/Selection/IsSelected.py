from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get selection.
selection = omni.usd.get_context().get_selection()

pathStr = '/World'
selectedF = selection.is_prim_path_selected(pathStr)
if selectedF:
    print('[' + pathStr + ' ] Selected')
else:
    print('[' + pathStr + ' ] Not selected')


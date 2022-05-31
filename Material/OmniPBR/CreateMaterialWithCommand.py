from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit.commands

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create new material.
omni.kit.commands.execute('CreateAndBindMdlMaterialFromLibrary', mdl_name='OmniPBR.mdl',
	mtl_name='OmniPBR', mtl_created_list=['/World/Looks/OmniPBR'])

# Get selection.
selection = omni.usd.get_context().get_selection()
selectedPaths = selection.get_selected_prim_paths()

# Path of the added material.
selectPrimPath = ""
for path in selectedPaths:
    selectPrimPath = path
    break

print(selectPrimPath)
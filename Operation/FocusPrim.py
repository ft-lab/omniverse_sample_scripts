# "omni.kit.viewport_legacy" is no longer available in kit 104.
#import omni.kit.viewport_legacy
import omni.ui.scene
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

#try:
#    viewport = omni.kit.viewport_legacy.get_viewport_interface()
#    if viewport != None:
#        viewport.get_viewport_window().focus_on_selected()
#except:
#    pass

#scene_view = omni.ui.scene.SceneView()
# Pass the real object, as a weak-reference will be retained
#viewport_api.add_scene_view(scene_view)
#print(dir(scene_view))

camera = UsdGeom.Camera().GetCamera()
print(camera)

'''
import omni.kit.commands
from pxr import Sdf, Usd

# Get current camera.
currentCameraPath = "/OmniverseKit_Persp"

# Aspect ratio.
aspect = 1.77777777

# Taret prim path.
targetPrim = "/World/Sphere"

omni.kit.commands.execute('FramePrimsCommand',
	prim_to_move=Sdf.Path(currentCameraPath),
	prims_to_frame=[targetPrim],
	time_code=Usd.TimeCode(),
	usd_context_name='',
	aspect_ratio=aspect)

'''


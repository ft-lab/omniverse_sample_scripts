from pxr import Usd, UsdGeom, CameraUtil, UsdShade, UsdSkel, Sdf, Gf, Tf
import omni.ext
import omni.ui
from omni.ui import color as cl
from omni.ui import scene as sc
import omni.kit
import omni.kit.app
import carb.events
from pathlib import Path
import time

# Kit104 : changed from omni.kit.viewport_legacy to omni.kit.viewport.utility.get_active_viewport_window
import omni.kit.viewport.utility

# Reference : https://github.com/NVIDIA-Omniverse/kit-extension-sample-ui-scene

# -------------------------------------.
# Scene draw process.
# -------------------------------------.
class SceneDraw (sc.Manipulator):
    _viewport_api = None

    def __init__(self, viewport_api, **kwargs):
        super().__init__ (**kwargs)

        # Set Viewport API.
        self._viewport_api = viewport_api

    # -------------------------------------------.
    # Repaint.
    # -------------------------------------------.
    def on_build (self):
        stage = omni.usd.get_context().get_stage()

        # Get selection.
        selection = omni.usd.get_context().get_selection()
        paths = selection.get_selected_prim_paths()

        time_code = Usd.TimeCode.Default()
        xformCache = UsdGeom.XformCache(time_code)

        for path in paths:
            prim = stage.GetPrimAtPath(path)
            if prim.IsValid():
                # Get world Transform.
                globalPose = xformCache.GetLocalToWorldTransform(prim)

                # Decompose transform.
                translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

                # World to NDC space (X : -1.0 to +1.0, Y : -1.0 to +1.0).
                ndc_pos = self._viewport_api.world_to_ndc.Transform(translate)

                # Translation matrix.
                moveT = sc.Matrix44.get_translation_matrix(ndc_pos[0], ndc_pos[1], 0.0)

                # Draw prim name.
                with sc.Transform(transform=moveT):
                    sc.Label(prim.GetName(), alignment = omni.ui.Alignment.CENTER, color=cl("#ffff00a0"), size=20)

# ----------------------------------------------------------.
class UISceneShowPrimNameExtension(omni.ext.IExt):
    _scene_view = None
    _stage = None
    _sceneDraw = None
    _time = 0
    _selectedPrimPaths = None
    _active_vp_window = None
    _viewport_api = None
    _active_viewport_name = ""
    _ext_id = ""

    # ------------------------------------------------.
    # Update event.
    # Update when selection shape changes.
    # Update when the active viewport is switched.
    # ------------------------------------------------.
    def on_update (self, e: carb.events.IEvent):
        # Check every 0.2 seconds.
        curTime = time.time()
        diffTime = curTime - self._time
        if diffTime > 0.2:
            self._time = curTime

            # Get selection.
            selection = omni.usd.get_context().get_selection()
            paths = selection.get_selected_prim_paths()

            # Selection changed.
            if self._selectedPrimPaths == None or self._selectedPrimPaths != paths:
                self._selectedPrimPaths = paths

                # Update drawing.
                if self._sceneDraw != None:
                    self._sceneDraw.invalidate()

            # If the active viewport name has changed.
            active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
            if active_vp_window != None and active_vp_window.name != self._active_viewport_name:
                # Rebuild overlay.
                self.term_window()
                self.init_window(self._ext_id)

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self, ext_id : str):
        self._ext_id = ext_id

        # Get current stage.
        self._stage = omni.usd.get_context().get_stage()

        self._time = time.time()

        # Kit104 : Get active viewport window.
        self._active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()

        # Get viewport API.
        self._viewport_api = self._active_vp_window.viewport_api

        # Register a callback to be called when the camera in the viewport is changed.
        self._subs_viewport_change = self._viewport_api.subscribe_to_view_change(self._viewport_changed)

        with self._active_vp_window.get_frame(ext_id):
            self._scene_view = sc.SceneView()

            # Add the manipulator into the SceneView's scene
            with self._scene_view.scene:
                ObjectInfoManipulator(model=ObjectInfoModel())

            # Register the SceneView with the Viewport to get projection and view updates
            self._viewport_api.add_scene_view(self._scene_view)

    # ------------------------------------------------.
    # Term window.
    # ------------------------------------------------.
    def term_window (self):
        if self._scene_view:
            # Empty the SceneView of any elements it may have
            self._scene_view.scene.clear()
            # Be a good citizen, and un-register the SceneView from Viewport updates
            if self._active_vp_window:
                self._active_vp_window.viewport_api.remove_scene_view(self._scene_view)

        self._active_vp_window = None

    # ------------------------------------------------.
    # Startup.
    # ------------------------------------------------.
    def on_startup(self, ext_id):
        self.init_window(ext_id)

    # ------------------------------------------------.
    # Shutdown.
    # ------------------------------------------------.
    def on_shutdown(self):
        self.term_window()

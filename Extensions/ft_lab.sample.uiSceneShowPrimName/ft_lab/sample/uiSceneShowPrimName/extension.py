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

# -------------------------------------.
# Scene draw process.
# -------------------------------------.
class SceneDraw (sc.Manipulator):
    _viewport_api = None

    def __init__(self, **kwargs):
        super().__init__ (**kwargs)

        # Kit104 : Get active viewport window.
        active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()

        # Get viewport API.
        self._viewport_api = active_vp_window.viewport_api

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
    _window = None
    _scene_view = None
    _objects_changed_listener = None
    _subs_update = None
    _stage = None
    _sceneDraw = None
    _time = 0
    _selectedPrimPaths = None

    # ------------------------------------------------.
    # Notification of object changes.
    # ------------------------------------------------.
    def _notice_objects_changed (self, notice, stage):
        # Update drawing.
        self._sceneDraw.invalidate()

    # ------------------------------------------------.
    # Update event.
    # Update when selection shape changes.
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
                self._sceneDraw.invalidate()

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self):
        # Get current stage.
        self._stage = omni.usd.get_context().get_stage()

        # Notification of object changes.
        self._objects_changed_listener = Tf.Notice.Register(
            Usd.Notice.ObjectsChanged, self._notice_objects_changed, self._stage)

        # Register for update event.
        self._subs_update = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(self.on_update)

        self._time = time.time()

        # Get main window viewport.
        self._window = omni.ui.Window('Viewport')

        with self._window.frame:
            with omni.ui.VStack():
                # The coordinate system is NDC space.
                # (X : -1.0 to +1.0, Y : -1.0 to +1.0).
                self._scene_view = sc.SceneView(aspect_ratio_policy=sc.AspectRatioPolicy.STRETCH)

                with self._scene_view.scene:
                    self._sceneDraw = SceneDraw()
                    self._sceneDraw.invalidate()

    # ------------------------------------------------.
    # Term window.
    # ------------------------------------------------.
    def term_window (self):
        if self._objects_changed_listener:
            self._objects_changed_listener.Revoke()

        self._window = None
        self._objects_changed_listener = None
        self._subs_update = None

    # ------------------------------------------------.
    # Startup.
    # ------------------------------------------------.
    def on_startup(self, ext_id):
        self.init_window()

    # ------------------------------------------------.
    # Shutdown.
    # ------------------------------------------------.
    def on_shutdown(self):
        self.term_window()

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
    _window = None
    _scene_view = None
    _objects_changed_listener = None
    _subs_update = None
    _stage = None
    _sceneDraw = None
    _time = 0
    _selectedPrimPaths = None
    _viewport_api = None
    _subs_viewport_change = None
    _active_viewport_name = ""

    # ------------------------------------------------.
    # Notification of object changes.
    # ------------------------------------------------.
    def _notice_objects_changed (self, notice, stage):
        # Update drawing.
        if self._sceneDraw != None:
            self._sceneDraw.invalidate()

    # ------------------------------------------------.
    # Called when the camera in the viewport is changed.
    # ------------------------------------------------.
    def _viewport_changed (self, viewport_api):
        # Update drawing.
        if self._sceneDraw != None:
            self._sceneDraw.invalidate()

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
                self.init_window()

    # ------------------------------------------------.
    # Called when the focus of the viewport changes.
    # The following are not called.
    # ------------------------------------------------.
    def _focused_changed (self, focused: bool):
        pass
        # If the active viewport name has changed.
        #active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
        #if active_vp_window != None and active_vp_window.name != self._active_viewport_name:
        #    # Rebuild overlay.
        #    self.term_window()
        #    self.init_window()

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

        # Kit104 : Get active viewport window.
        active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()

        # Get viewport API.
        self._viewport_api = active_vp_window.viewport_api

        # Called when the focus of the viewport changes.
        # The following are disabled because they are unstable.
        #active_vp_window.set_focused_changed_fn(self._focused_changed)

        # Register a callback to be called when the camera in the viewport is changed.
        self._subs_viewport_change = self._viewport_api.subscribe_to_view_change(self._viewport_changed)

        # Get viewport window.
        self._active_viewport_name = active_vp_window.name   # "Viewport", "Viewport 2" etc.
        self._window = omni.ui.Window(self._active_viewport_name)

        with self._window.frame:
            with omni.ui.VStack():
                # The coordinate system is NDC space.
                # (X : -1.0 to +1.0, Y : -1.0 to +1.0).
                self._scene_view = sc.SceneView(aspect_ratio_policy=sc.AspectRatioPolicy.STRETCH)

                with self._scene_view.scene:
                    self._sceneDraw = SceneDraw(self._viewport_api)

                    # Update drawing.
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
        self._subs_viewport_change = None

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

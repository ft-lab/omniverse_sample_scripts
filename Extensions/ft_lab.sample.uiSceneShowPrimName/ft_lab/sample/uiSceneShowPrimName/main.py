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

# -------------------------------------.
# Scene draw process.
# -------------------------------------.
class SceneDraw (sc.Manipulator):
    def __init__(self, **kwargs):
        super().__init__ (**kwargs)

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

                # Draw prim name.
                moveT = sc.Matrix44.get_translation_matrix(translate[0], translate[1], translate[2])
                with sc.Transform(transform=moveT):
                    sc.Label(prim.GetName(), alignment = omni.ui.Alignment.CENTER, color=cl("#ffff00a0"), size=20)

        #self.invalidate()

# ----------------------------------------------------------.
class UISceneShowPrimNameExtension(omni.ext.IExt):
    _window = None
    _scene_view = None
    _objects_changed_listener = None
    _subs_update = None
    _camera_path = None
    _stage = None
    _sceneDraw = None
    _time = 0
    _selectedPrimPaths = None

    # ------------------------------------------------.
    # Get current camera prim path.
    # ------------------------------------------------.
    def getCurrentCameraPrimPath (self):
        # Get viewport.
        # Kit103 changed from omni.kit.viewport to omni.kit.viewport_legacy
        viewport = omni.kit.viewport_legacy.get_viewport_interface()
        viewportWindow = viewport.get_viewport_window()

        # Get active camera path.
        cameraPath = viewportWindow.get_active_camera()
        return cameraPath

    # ------------------------------------------------.
    # Get View/Projection Matrix of the current camera.
    # ------------------------------------------------.
    def getCurrentCameraViewProjectionMatrix (self):
        # Get current camera Prim Path.
        if self._camera_path == None:
            self._camera_path = self.getCurrentCameraPrimPath()

        if self._stage == None:
            self._stage = omni.usd.get_context().get_stage()

        viewMatrix = None
        projMatrix = None

        # Get active camera.
        cameraPrim = self._stage.GetPrimAtPath(self._camera_path)
        if cameraPrim.IsValid():
            camera  = UsdGeom.Camera(cameraPrim)                # UsdGeom.Camera
            cameraV = camera.GetCamera(Usd.TimeCode.Default())  # Gf.Camera
            viewMatrix = cameraV.frustum.ComputeViewMatrix()
            projMatrix = cameraV.frustum.ComputeProjectionMatrix()

        return viewMatrix, projMatrix


    # ------------------------------------------------.
    # Camera change event called from Tf.Notice (Usd.Notice.ObjectsChanged).
    # ------------------------------------------------.
    def _camera_changed (self):
        # Called when the camera is changed.
        def flatten (transform):
            # Convert array[n][m] to array[n*m].
            return [item for sublist in transform for item in sublist]
    
        # Get View/Projection Matrix.
        view, projection = self.getCurrentCameraViewProjectionMatrix()

        # Convert Gf.Matrix4d to list　
        view = flatten(view)
        projection = flatten(projection)

        # Set the scene
        if self._scene_view != None:
            self._scene_view.model.view = view
            self._scene_view.model.projection = projection

    def _notice_objects_changed (self, notice, stage):
        self._camera_path = self.getCurrentCameraPrimPath()

        # Update drawing.
        self._sceneDraw.invalidate()

        # Called by Tf.Notice.
        for p in notice.GetChangedInfoOnlyPaths():
            if p.GetPrimPath() == self._camera_path:
                self._camera_changed()

    # ------------------------------------------------.
    # Update event.
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
        imagesPath = Path(__file__).parent.joinpath("images")

        # Get current stage.
        self._stage = omni.usd.get_context().get_stage()

        # Get current camera Prim Path.
        self._camera_path = self.getCurrentCameraPrimPath()

        # Tracking the camera
        self._objects_changed_listener = Tf.Notice.Register(
            Usd.Notice.ObjectsChanged, self._notice_objects_changed, self._stage)

        # Register for update event.
        self._subs_update = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(self.on_update)

        self._time = time.time()

        # Get main window viewport.
        self._window = omni.ui.Window('Viewport')

        with self._window.frame:
            with omni.ui.VStack():
                self._scene_view = sc.SceneView()

                # Update view./projection matrix.
                self._camera_changed()

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

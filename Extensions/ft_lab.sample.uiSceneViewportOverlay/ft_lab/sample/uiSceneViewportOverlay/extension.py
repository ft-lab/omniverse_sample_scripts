from pxr import Usd, UsdGeom, CameraUtil, UsdShade, Sdf, Gf, Tf
import omni.ext
import omni.ui
from omni.ui import color as cl
from omni.ui import scene as sc
import omni.kit
from pathlib import Path
import math

# Kit104 : changed from omni.kit.viewport_legacy to omni.kit.viewport.utility.get_active_viewport_window
import omni.kit.viewport.utility

# ----------------------------------------------------------.
class UISceneViewportOverlayExtension(omni.ext.IExt):
    _window = None
    _scene_view = None
    _objects_changed_listener = None
    _camera_path = None
    _stage = None
    _viewport_api = None
    _active_viewport_name = ""

    # ------------------------------------------------.
    # Get View/Projection Matrix of the current camera.
    # ------------------------------------------------.
    def getCurrentCameraViewProjectionMatrix (self):
        # Get current camera Prim Path.
        if self._camera_path == None:
            self._camera_path = self._viewport_api.camera_path.pathString

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

    # ------------------------------------------------.
    # Notification of object changes.
    # ------------------------------------------------.
    def _notice_objects_changed (self, notice, stage):
        # Camera changed.
        self._camera_path = self._viewport_api.camera_path.pathString

        # Called by Tf.Notice.
        for p in notice.GetChangedInfoOnlyPaths():
            if p.GetPrimPath() == self._camera_path:
                self._camera_changed()

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self):
        imagesPath = Path(__file__).parent.joinpath("images")

        # Get current stage.
        self._stage = omni.usd.get_context().get_stage()

        # Kit104 : Get active viewport window.
        active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
        self._viewport_api = active_vp_window.viewport_api

        # Get camera path ("/OmniverseKit_Persp" etc).
        self._camera_path = self._viewport_api.camera_path.pathString

        # Tracking the camera
        self._objects_changed_listener = Tf.Notice.Register(
            Usd.Notice.ObjectsChanged, self._notice_objects_changed, self._stage)

        # Get viewport window.
        self._active_viewport_name = active_vp_window.name   # "Viewport", "Viewport 2" etc.
        self._window = omni.ui.Window(self._active_viewport_name)

        with self._window.frame:
            with omni.ui.VStack():
                self._scene_view = sc.SceneView()

                # Update view./projection matrix.
                self._camera_changed()

                with self._scene_view.scene:
                    # Edges of cube
                    cubeSize = 100.0
                    sc.Line([-cubeSize, -cubeSize, -cubeSize], [cubeSize, -cubeSize, -cubeSize])
                    sc.Line([-cubeSize, cubeSize, -cubeSize], [cubeSize, cubeSize, -cubeSize])
                    sc.Line([-cubeSize, -cubeSize, cubeSize], [cubeSize, -cubeSize, cubeSize])
                    sc.Line([-cubeSize, cubeSize, cubeSize], [cubeSize, cubeSize, cubeSize])

                    sc.Line([-cubeSize, -cubeSize, -cubeSize], [-cubeSize, cubeSize, -cubeSize])
                    sc.Line([cubeSize, -cubeSize, -cubeSize], [cubeSize, cubeSize, -cubeSize])
                    sc.Line([-cubeSize, -cubeSize, cubeSize], [-cubeSize, cubeSize, cubeSize])
                    sc.Line([cubeSize, -cubeSize, cubeSize], [cubeSize, cubeSize, cubeSize])

                    sc.Line([-cubeSize, -cubeSize, -cubeSize], [-cubeSize, -cubeSize, cubeSize])
                    sc.Line([-cubeSize, cubeSize, -cubeSize], [-cubeSize, cubeSize, cubeSize])
                    sc.Line([cubeSize, -cubeSize, -cubeSize], [cubeSize, -cubeSize, cubeSize])
                    sc.Line([cubeSize, cubeSize, -cubeSize], [cubeSize, cubeSize, cubeSize])

                    # Use Transform to change position.
                    moveT = sc.Matrix44.get_translation_matrix(0, 0, 0)
                    with sc.Transform(transform=moveT):
                        sc.Label("Hello Omniverse !!", alignment = omni.ui.Alignment.CENTER, color=cl("#ffff00a0"), size=20)

    # ------------------------------------------------.
    # Term window.
    # ------------------------------------------------.
    def term_window (self):
        if self._objects_changed_listener:
            self._objects_changed_listener.Revoke()

        self._window = None
        self._objects_changed_listener = None

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

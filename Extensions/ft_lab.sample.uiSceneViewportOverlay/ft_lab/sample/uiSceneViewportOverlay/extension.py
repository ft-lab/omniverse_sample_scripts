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

# Reference : https://github.com/NVIDIA-Omniverse/kit-extension-sample-ui-scene

# ----------------------------------------------------------.
class UISceneViewportOverlayExtension(omni.ext.IExt):
    _scene_view = None
    _stage = None
    _viewport_api = None
    _active_vp_window = None

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self, ext_id : str):
        imagesPath = Path(__file__).parent.joinpath("images")

        # Get current stage.
        self._stage = omni.usd.get_context().get_stage()

        # Kit104 : Get active viewport window.
        self._active_vp_window = omni.kit.viewport.utility.get_active_viewport_window()
        self._viewport_api = self._active_vp_window.viewport_api

        with self._active_vp_window.get_frame(ext_id):
            self._scene_view = sc.SceneView()

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

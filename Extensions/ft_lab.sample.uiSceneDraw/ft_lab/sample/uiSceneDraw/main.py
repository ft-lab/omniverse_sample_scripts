import omni.ext
import omni.ui
from omni.ui import color as cl
from omni.ui import scene as sc
from pathlib import Path
import math

# -------------------------------------.
# Scene draw process.
# -------------------------------------.
class SceneDraw(sc.Manipulator):
    _angle1 = 0.0
    _angle2 = 0.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._angle1 = 0.0
        self._angle2 = 45.0

    def on_build(self):
        # Consider the order. This uses the z-value Depth.
        # -1.0 < depth <= 0.0
        
        depth = 0.0
        moveT = sc.Matrix44.get_translation_matrix(0.0, 0.0, depth)
        with sc.Transform(transform=moveT):
            sc.Rectangle(2.0, 2.0, wireframe=False, color=cl("#003000"))

        depth = -0.1
        rotT  = sc.Matrix44.get_rotation_matrix(0, 0, self._angle1, True)
        moveT = sc.Matrix44.get_translation_matrix(0.25, 0.3, depth)
        viewT = moveT * rotT
        with sc.Transform(transform=viewT):
            sc.Rectangle(1.5, 0.15, wireframe=False, color=cl("#3030ff"))

        depth = -0.15
        rotT  = sc.Matrix44.get_rotation_matrix(0, 0, self._angle2, True)
        moveT = sc.Matrix44.get_translation_matrix(-0.25, -0.1, depth)
        viewT = moveT * rotT
        with sc.Transform(transform=viewT):
            sc.Rectangle(1.5, 0.15, wireframe=False, color=cl("#ff3030"))

        self._angle1 = math.fmod(self._angle1 + 0.2, 360.0)
        self._angle2 = math.fmod(self._angle2 + 0.1, 360.0)

        self.invalidate()

# ----------------------------------------------------------.
class UISceneExtension(omni.ext.IExt):
    _window = None
    _scene_view = None

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self):
        imagesPath = Path(__file__).parent.joinpath("images")

        # Create new window.
        self._window = omni.ui.Window("UI Scene Draw Window", width=400, height=400)

        # ------------------------------------------.
        with self._window.frame:
            # Create window UI.
            with omni.ui.VStack(height=0):
                omni.ui.Spacer(height=4)
                omni.ui.Label("Use omni.ui.scene for custom drawing.") 
                omni.ui.Spacer(height=4)

                self._scene_view = sc.SceneView(
                    aspect_ratio_policy=sc.AspectRatioPolicy.PRESERVE_ASPECT_FIT,
                    height=300
                )

                with self._scene_view.scene:
                    SceneDraw()

    # ------------------------------------------------.
    # Term window.
    # ------------------------------------------------.
    def term_window (self):
        if self._window != None:
            self._window = None

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

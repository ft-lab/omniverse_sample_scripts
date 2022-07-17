import omni.ext
import omni.ui
from omni.ui import color as cl
from omni.ui import scene as sc
from pathlib import Path

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
        self._window = omni.ui.Window("UI Scene Window", width=300, height=400)

        # ------------------------------------------.
        with self._window.frame:
            # Create window UI.
            with omni.ui.VStack(height=0):
                omni.ui.Spacer(height=4)
                omni.ui.Label("Use omni.ui.scene for custom drawing.") 
                omni.ui.Spacer(height=4)

                self._scene_view = sc.SceneView(
                    aspect_ratio_policy=sc.AspectRatioPolicy.PRESERVE_ASPECT_FIT,
                    height=200
                )

                with self._scene_view.scene:
                    sc.Line([-1.0, -1.0, 0], [1.0, 1.0, 0], color=cl.red, thickness=2)
                    sc.Line([-1.0, 1.0, 0], [1.0, -1.0, 0], color=cl.green, thickness=1)
                    sc.Arc(0.5, color=cl("#5040ff"))
                    sc.Rectangle(0.3, 0.3, wireframe=False, color=cl("#c0ff00"))

                    # Use Transform to change position.
                    moveT = sc.Matrix44.get_translation_matrix(0.0, -0.8, 0)
                    with sc.Transform(transform=moveT):
                        sc.Label("Test", alignment = omni.ui.Alignment.CENTER, color=cl.black, size=20)

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

from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf
import omni.ext
from pathlib import Path

class LoadStageExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[ft_lab.sample.loadStage] LoadStageExtension startup")

        # Get USD file.
        usdPath = Path(__file__).parent.joinpath("usd")
        usdFile = f"{usdPath}/test.usd"

        # Load stage.
        omni.usd.get_context().open_stage(usdFile)

    def on_shutdown(self):
        print("[ft_lab.sample.loadStage] LoadStageExtension shutdown")

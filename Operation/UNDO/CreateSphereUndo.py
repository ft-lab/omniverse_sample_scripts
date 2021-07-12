from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.kit.commands
import omni.kit.undo

# Get stage.
stage = omni.usd.get_context().get_stage()

# Process to create a sphere.
class MyCreateSphere (omni.kit.commands.Command):
    _path = ""

    def __init__ (self, path):
        self._path = path

    def do (self):
        sphereGeom = UsdGeom.Sphere.Define(stage, self._path)

        # Set radius.
        sphereGeom.CreateRadiusAttr(5.0)

        # Set color.
        sphereGeom.CreateDisplayColorAttr([(1.0, 0.0, 0.0)])

        # Set position.
        UsdGeom.XformCommonAPI(sphereGeom).SetTranslate((0.0, 5.0, 0.0))

    def undo (self):
        stage.RemovePrim(self._path)

# Create sphere.
pathName = '/World/sphere'

# Register a Class and run it.
omni.kit.commands.register(MyCreateSphere)
omni.kit.commands.execute("MyCreateSphere", path=pathName)

# UNDO.
omni.kit.undo.undo()

# REDO.
omni.kit.undo.redo()

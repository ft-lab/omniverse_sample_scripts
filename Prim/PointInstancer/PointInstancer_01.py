from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import random

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString

# Create empty node(Xform).
path = defaultPrimPath + '/trees'
UsdGeom.Xform.Define(stage, path)
prim = stage.GetPrimAtPath(path)

# Create PointInstancer.
pointInstancerPath = path + '/pointInstancer'
pointInstancer = UsdGeom.PointInstancer.Define(stage, pointInstancerPath)

# Create Reference.
refPath = pointInstancerPath + '/asset'
UsdGeom.Xform.Define(stage, refPath)
prim = stage.GetPrimAtPath(refPath)

# Set Kind.
Usd.ModelAPI(prim).SetKind(Kind.Tokens.component)

# Set the asset to be referenced.
pointInstancer.CreatePrototypesRel().AddTarget(refPath)

# Remove references.
prim.GetReferences().ClearReferences()

# Add a reference.
#usdPath = "./simpleTree.usda"
usdPath = "https://ft-lab.github.io/usd/omniverse/usd/simpleTree.usda"
prim.GetReferences().AddReference(usdPath)

# Points data.
positions = []
scales = []
protoIndices = []
orientations = []
areaSize = 1000.0
treesCou = 50
for i in range(treesCou):
    px = random.random() * areaSize - (areaSize * 0.5)
    pz = random.random() * areaSize - (areaSize * 0.5)
    scale = random.random() * 0.5 + 0.8

    positions.append(Gf.Vec3f(px, 0.0, pz))        # Position.
    orientations.append(Gf.Quath())                # Rotation.
    scales.append(Gf.Vec3f(scale, scale, scale))   # Scale.
    protoIndices.append(0)                         # asset index.

pointInstancer.CreatePositionsAttr(positions)
pointInstancer.CreateOrientationsAttr(orientations)
pointInstancer.CreateScalesAttr(scales)
pointInstancer.CreateProtoIndicesAttr(protoIndices)


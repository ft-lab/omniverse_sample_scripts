from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString

# Create sphere.
orgPath = defaultPrimPath + '/org'
UsdGeom.Xform.Define(stage, orgPath)
spherePath = orgPath + '/sphere'
sphereGeom = UsdGeom.Sphere.Define(stage, spherePath)

# Set radius.
sphereGeom.CreateRadiusAttr(2.0)

# Set color.
sphereGeom.CreateDisplayColorAttr([(1.0, 0.0, 0.0)])

# Create empty node(Xform).
path = defaultPrimPath + '/refShape'
UsdGeom.Xform.Define(stage, path)
prim = stage.GetPrimAtPath(path)

# Set position.
UsdGeom.XformCommonAPI(prim).SetTranslate((5.0, 0.0, 0.0))

# Remove references.
prim.GetReferences().ClearReferences()

# Add a internal reference.
# The Path to be added must be an Xform.
prim.GetReferences().AddInternalReference(orgPath)

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Get root path.
rootPath = '/'
if defaultPrim.IsValid():
    rootPath = defaultPrim.GetPath().pathString

# Create mesh.
meshGeom = UsdGeom.Mesh.Define(stage, rootPath + "/mesh")

# Set vertices.
meshGeom.CreatePointsAttr([(-10, 0, -10), (-10, 0, 10), (10, 0, 10), (10, 0, -10)])

# Set normals.
meshGeom.CreateNormalsAttr([(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)])
meshGeom.SetNormalsInterpolation("vertex")

# Set face vertex count.
meshGeom.CreateFaceVertexCountsAttr([4])

# Set face vertex indices.
meshGeom.CreateFaceVertexIndicesAttr([0, 1, 2, 3])

# Set uvs.
# USD 22.11 : The specification has been changed to use UsdGeom.PrimvarsAPI.
primvarV = UsdGeom.PrimvarsAPI(meshGeom).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.vertex)
attr = primvarV.GetAttr()
attr.Set([(0, 1), (0, 0), (1, 0), (1, 1)])

# Subdivision is set to none.
meshGeom.CreateSubdivisionSchemeAttr().Set("none")

# Set position.
UsdGeom.XformCommonAPI(meshGeom).SetTranslate((0.0, 0.0, 0.0))

# Set rotation.
UsdGeom.XformCommonAPI(meshGeom).SetRotate((0.0, 0.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

# Set scale.
UsdGeom.XformCommonAPI(meshGeom).SetScale((1.0, 1.0, 1.0))

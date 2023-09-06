from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Get root path.
rootPath = '/'
if defaultPrim.IsValid():
    rootPath = defaultPrim.GetPath().pathString

# ------------------------------------------------.
# Create mesh.
# @param[in] path            Prim path.
# @param[in] interpolation   "vertex" or "faceVarying".
# ------------------------------------------------.
def createTestMesh (path : str, interpolation : str = "vertex", pos : Gf.Vec3f = Gf.Vec3f(0, 0, 0)):
    if interpolation != "vertex" and interpolation != "faceVarying":
        return

    # Create mesh.
    meshGeom = UsdGeom.Mesh.Define(stage, path)

    # Set vertices.
    meshGeom.CreatePointsAttr([(-10, 0, -10), (0, 0, -10), (10, 0, -10), (-10, 0, 0), (0, 0, 0), (10, 0, 0)])

    # Set face vertex count.
    meshGeom.CreateFaceVertexCountsAttr([4, 4])

    # Set face vertex indices.
    meshGeom.CreateFaceVertexIndicesAttr([0, 3, 4, 1, 1, 4, 5, 2])

    if interpolation == "vertex":
        # Set normals and UVs for each vertex.

        # Set normals.
        meshGeom.CreateNormalsAttr([(0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0)])
        meshGeom.SetNormalsInterpolation("vertex")

        # Set uvs.
        # USD 22.11 : The specification has been changed to use UsdGeom.PrimvarsAPI.
        primvarV = UsdGeom.PrimvarsAPI(meshGeom).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.vertex)
        attr = primvarV.GetAttr()
        attr.Set([(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (0.0, 0.0), (1.0, 0.0), (2.0, 0.0)])

    else:
        # Set normals and UVs for each face vertex.

        # Set normals.
        normalList = []
        for i in range(2):
            normalList.extend([(0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0)])
        meshGeom.CreateNormalsAttr(normalList)
        meshGeom.SetNormalsInterpolation("faceVarying")

        # Set uvs.
        primvarV = UsdGeom.PrimvarsAPI(meshGeom).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying)
        attr = primvarV.GetAttr()

        uvsList = []
        uvsList.extend([(0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0)])
        uvsList.extend([(1.0, 1.0), (1.0, 0.0), (2.0, 0.0), (2.0, 1.0)])
        attr.Set(uvsList)

    # Subdivision is set to none.
    meshGeom.CreateSubdivisionSchemeAttr().Set("none")

    # Set position.
    UsdGeom.XformCommonAPI(meshGeom).SetTranslate((pos[0], pos[1], pos[2]))

    # Set rotation.
    UsdGeom.XformCommonAPI(meshGeom).SetRotate((0.0, 0.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

    # Set scale.
    UsdGeom.XformCommonAPI(meshGeom).SetScale((1.0, 1.0, 1.0))

# -----------------------------------------------.
createTestMesh(rootPath + "/mesh_vertex", "vertex", Gf.Vec3f(0, 0, 0))
createTestMesh(rootPath + "/mesh_faceVarying", "faceVarying", Gf.Vec3f(0, 0, 20))


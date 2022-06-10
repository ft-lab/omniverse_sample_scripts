from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Get root path.
rootPath = '/'
if defaultPrim.IsValid():
    rootPath = defaultPrim.GetPath().pathString

# --------------------------------------.
# Create new Material (OmniPBR).
# @param[in] materialPrimPath   Prim path of Material
# @param[in] diffuseColor       Diffuse color.
# --------------------------------------.
def createMaterialOmniPBR (materialPrimPath : str, diffuseColor : Gf.Vec3f):
    material = UsdShade.Material.Define(stage, materialPrimPath)

    shaderPath = materialPrimPath + '/Shader'
    shader = UsdShade.Shader.Define(stage, shaderPath)
    shader.SetSourceAsset('OmniPBR.mdl', 'mdl')
    shader.GetPrim().CreateAttribute('info:mdl:sourceAsset:subIdentifier', Sdf.ValueTypeNames.Token, False, Sdf.VariabilityUniform).Set('OmniPBR')

    # Set Diffuse color.
    shader.CreateInput('diffuse_color_constant', Sdf.ValueTypeNames.Color3f).Set(diffuseColor)

    # Connecting Material to Shader.
    mdlOutput = material.CreateSurfaceOutput('mdl')
    mdlOutput.ConnectToSource(shader, 'out')

    return materialPrimPath

# --------------------------------------.
# Create mesh with subset.
# --------------------------------------.
def createMesh (meshPath : str):
    # Create mesh.
    meshGeom = UsdGeom.Mesh.Define(stage, meshPath)

    # Set vertices.
    meshGeom.CreatePointsAttr([(-10, 0, -10), (0, 0, -10), (10, 0, -10), (-10, 0, 0), (0, 0, 0), (10, 0, 0)])

    # Set face vertex count.
    meshGeom.CreateFaceVertexCountsAttr([4, 4])

    # Set face vertex indices.
    meshGeom.CreateFaceVertexIndicesAttr([0, 3, 4, 1, 1, 4, 5, 2])

    # Set normals and UVs for each face vertex.

    # Set normals.
    normalList = []
    for i in range(2):
        normalList.extend([(0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0)])
    meshGeom.CreateNormalsAttr(normalList)
    meshGeom.SetNormalsInterpolation("faceVarying")

    # Set uvs.
    uvsList = []
    uvsList.extend([(0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0)])
    uvsList.extend([(1.0, 1.0), (1.0, 0.0), (2.0, 0.0), (2.0, 1.0)])
    texCoords = meshGeom.CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying)
    texCoords.Set(uvsList)

    # Subdivision is set to none.
    meshGeom.CreateSubdivisionSchemeAttr().Set("none")

    # Set position.
    UsdGeom.XformCommonAPI(meshGeom).SetTranslate((0.0, 0.0, 0.0))

    # Set rotation.
    UsdGeom.XformCommonAPI(meshGeom).SetRotate((0.0, 0.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

    # Set scale.
    UsdGeom.XformCommonAPI(meshGeom).SetScale((1.0, 1.0, 1.0))

    # Create subset 1.
    subsetPath = meshPath + "/submesh_1"
    geomSubset1 = UsdGeom.Subset.Define(stage, subsetPath)

    geomSubset1.CreateFamilyNameAttr("materialBind")
    geomSubset1.CreateElementTypeAttr("face")
    geomSubset1.CreateIndicesAttr([0])  # Set the index on the face.

    # Bind material.
    matPrim = stage.GetPrimAtPath(rootPath + "/Looks/mat1")
    if matPrim.IsValid():
        UsdShade.MaterialBindingAPI(geomSubset1).Bind(UsdShade.Material(matPrim))

    # Create subset 2.
    subsetPath = meshPath + "/submesh_2"
    geomSubset2 = UsdGeom.Subset.Define(stage, subsetPath)

    geomSubset2.CreateFamilyNameAttr("materialBind")
    geomSubset2.CreateElementTypeAttr("face")
    geomSubset2.CreateIndicesAttr([1])  # Set the index on the face.

    # Bind material.
    matPrim = stage.GetPrimAtPath(rootPath + "/Looks/mat2")
    if matPrim.IsValid():
        UsdShade.MaterialBindingAPI(geomSubset2).Bind(UsdShade.Material(matPrim))

# -----------------------------------------------------------.
# Create scope.
looksScopePath = rootPath + "/Looks"
scopePrim = stage.GetPrimAtPath(looksScopePath)
if scopePrim.IsValid() == False:
    UsdGeom.Scope.Define(stage, looksScopePath)

# Create material.
createMaterialOmniPBR(rootPath + "/Looks/mat1", Gf.Vec3f(1.0, 0.0, 0.0))
createMaterialOmniPBR(rootPath + "/Looks/mat2", Gf.Vec3f(0.0, 1.0, 0.0))

# Create mesh.
createMesh(rootPath + "/mesh")
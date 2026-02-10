from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create mesh.
meshPath = '/World/mesh'
meshGeom = UsdGeom.Mesh.Define(stage, meshPath)
meshGeom.CreatePointsAttr([(-10, 0, -10), (-10, 0, 10), (10, 0, 10), (10, 0, -10)])
meshGeom.CreateNormalsAttr([(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)])
meshGeom.CreateFaceVertexCountsAttr([4])
meshGeom.CreateFaceVertexIndicesAttr([0, 1, 2, 3])
texCoords = UsdGeom.PrimvarsAPI(meshGeom).CreatePrimvar("st", 
        Sdf.ValueTypeNames.TexCoord2fArray, 
        UsdGeom.Tokens.varying)
texCoords.Set([(0, 1), (0, 0), (1, 0), (1, 1)])
meshPrim = stage.GetPrimAtPath(meshPath)

# Create material scope.
materialScopePath = '/World/Materials'
scopePrim = stage.GetPrimAtPath(materialScopePath)
if scopePrim.IsValid() == False:
    UsdGeom.Scope.Define(stage, materialScopePath)

# Create material (omniPBR).
materialPath = '/World/Materials/omniPBR_mat1'
material = UsdShade.Material.Define(stage, materialPath)

shaderPath = materialPath + '/Shader'
shader = UsdShade.Shader.Define(stage, shaderPath)
shader.SetSourceAsset('OmniPBR.mdl', 'mdl')
shader.GetPrim().CreateAttribute('info:mdl:sourceAsset:subIdentifier', Sdf.ValueTypeNames.Token, False, Sdf.VariabilityUniform).Set('OmniPBR')

# Set Diffuse color.
shader.CreateInput('diffuse_color_constant', Sdf.ValueTypeNames.Color3f).Set((1.0, 0.5, 0.4))

# Set Metallic.
shader.CreateInput('metallic_constant', Sdf.ValueTypeNames.Float).Set(0.0)

# Set Roughness.
shader.CreateInput('reflection_roughness_constant', Sdf.ValueTypeNames.Float).Set(0.2)

# Set Diffuse texture.
# Note : Texture files should be specified in the path where they exist.
#diffuseTextureFilePath = '../textures/stone_01_diffuse.png'
diffuseTextureFilePath = 'https://ft-lab.github.io/usd/omniverse/textures/stone_01_diffuse.png'
diffTexIn = shader.CreateInput('diffuse_texture', Sdf.ValueTypeNames.Asset)
diffTexIn.Set(diffuseTextureFilePath)
diffTexIn.GetAttr().SetColorSpace('sRGB')

# Set Diffuse value.
diffTintIn = shader.CreateInput('diffuse_tint', Sdf.ValueTypeNames.Color3f)
diffTintIn.Set((0.9, 0.9, 0.9))

# Set normal texture.
# Note : Texture files should be specified in the path where they exist.
#normalTextureFilePath = '../textures/stone_01_normal.png'
normalTextureFilePath = 'https://ft-lab.github.io/usd/omniverse/textures/stone_01_normal.png'
normalTexIn = shader.CreateInput('normalmap_texture', Sdf.ValueTypeNames.Asset)
normalTexIn.Set(normalTextureFilePath)

# The ColorSpace of the Normal map must be raw.
normalTexIn.GetAttr().SetColorSpace('raw')

# Normal strength.
normalStrengthIn = shader.CreateInput('bump_factor', Sdf.ValueTypeNames.Float)
normalStrengthIn.Set(1.0)

# Connecting Material to Shader.
mdlOutput = material.CreateSurfaceOutput('mdl')
mdlOutput.ConnectToSource(shader.ConnectableAPI(), 'out')

# Bind material.
UsdShade.MaterialBindingAPI(meshPrim).Bind(material)


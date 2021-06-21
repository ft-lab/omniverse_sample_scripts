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
texCoords = meshGeom.CreatePrimvar("st", 
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
#textureFilePath = 'K:/NVIDIA_omniverse/images/tile_image.png'
textureFilePath = '../textures/tile_image.png'
diffTexIn = shader.CreateInput('diffuse_texture', Sdf.ValueTypeNames.Asset)
diffTexIn.Set(textureFilePath)
diffTexIn.GetAttr().SetColorSpace('sRGB')

# Set Diffuse value.
diffTintIn = shader.CreateInput('diffuse_tint', Sdf.ValueTypeNames.Color3f)
diffTintIn.Set((0.9, 0.9, 0.9))

# Connecting Material to Shader.
mdlOutput = material.CreateSurfaceOutput('mdl')
mdlOutput.ConnectToSource(shader, 'out')

# Bind material.
UsdShade.MaterialBindingAPI(meshPrim).Bind(material)


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

# Create material (UsdPreviewSurface).
materialPath = '/World/Materials/mat1'
material = UsdShade.Material.Define(stage, materialPath)
pbrShader = UsdShade.Shader.Define(stage, materialPath + '/PBRShader')
pbrShader.CreateIdAttr("UsdPreviewSurface")
pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.2, 0.0))
pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

# Set diffuse texture.
stReader = UsdShade.Shader.Define(stage, materialPath + '/stReader')
stReader.CreateIdAttr('UsdPrimvarReader_float2')

diffuseTextureSampler = UsdShade.Shader.Define(stage, materialPath + '/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')

# Note : Texture files should be specified in the path where they exist.
#textureFilePath = 'K:/NVIDIA_omniverse/images/tile_image.png'
textureFilePath = '../textures/tile_image.png'
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set(textureFilePath)

diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')

stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
stInput.Set('st')
stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

# Connect PBRShader to Material.
material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

# Bind material.
UsdShade.MaterialBindingAPI(meshPrim).Bind(material)


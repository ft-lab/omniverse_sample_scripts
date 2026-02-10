from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create sphere.
spherePath = '/World/sphere'
sphereGeom = UsdGeom.Sphere.Define(stage, spherePath)
sphereGeom.CreateRadiusAttr(20.0)
spherePrim = stage.GetPrimAtPath(spherePath)
spherePrim.CreateAttribute('refinementEnableOverride', Sdf.ValueTypeNames.Bool).Set(True)
spherePrim.CreateAttribute('refinementLevel', Sdf.ValueTypeNames.Int).Set(2)

prim = sphereGeom.GetPrim()

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

# Connecting Material to Shader.
mdlOutput = material.CreateSurfaceOutput('mdl')
mdlOutput.ConnectToSource(shader.ConnectableAPI(), 'out')

# Bind material.
bindAPI = UsdShade.MaterialBindingAPI(prim)
bindAPI.Bind(material)
bindAPI.Apply(prim)


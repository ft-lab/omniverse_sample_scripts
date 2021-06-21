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

# Create material (UsdPreviewSurface).
materialPath = '/World/Materials/mat1'
material = UsdShade.Material.Define(stage, materialPath)
pbrShader = UsdShade.Shader.Define(stage, materialPath + '/PBRShader')
pbrShader.CreateIdAttr("UsdPreviewSurface")
pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.2, 0.0))
pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

# Connect PBRShader to Material.
material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

# Bind material.
UsdShade.MaterialBindingAPI(spherePrim).Bind(material)

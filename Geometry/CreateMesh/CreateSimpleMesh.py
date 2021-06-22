from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Create mesh.
meshGeom = UsdGeom.Mesh.Define(stage, "/World/mesh")

# Set vertices.
meshGeom.CreatePointsAttr([(-10, 0, -10), (-10, 0, 10), (10, 0, 10), (10, 0, -10)])

# Set normals.
meshGeom.CreateNormalsAttr([(0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0)])

# Set face vertex count.
meshGeom.CreateFaceVertexCountsAttr([4])

# Set face vertex indices.
meshGeom.CreateFaceVertexIndicesAttr([0, 1, 2, 3])

# Set uvs.
texCoords = meshGeom.CreatePrimvar("st", 
        Sdf.ValueTypeNames.TexCoord2fArray, 
        UsdGeom.Tokens.varying)
texCoords.Set([(0, 1), (0, 0), (1, 0), (1, 1)])

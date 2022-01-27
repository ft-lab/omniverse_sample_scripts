from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

# No need to normalize.
dirA = Gf.Vec3f(1.0, 0.0, 0.0).GetNormalized()
dirB = Gf.Vec3f(-0.2, 12.0, 15.0).GetNormalized()

print("dirA : " + str(dirA))
print("dirB : " + str(dirB))

# Calculate the rotation to transform dirA to dirB.
rot = Gf.Rotation().SetRotateInto(Gf.Vec3d(dirA), Gf.Vec3d(dirB))

# Check that rot is correct.
# v will have the same result as dirB.
m = Gf.Matrix4f(rot, Gf.Vec3f(0, 0, 0))
v = m.Transform(dirA)
print("dirA * m = " + str(v))

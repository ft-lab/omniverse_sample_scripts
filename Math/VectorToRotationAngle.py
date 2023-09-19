from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

dirV = Gf.Vec3f(20.0, 5.0, -25.0)

yUp = Gf.Vec3f(0, 1, 0)
m = Gf.Matrix4f().SetLookAt(Gf.Vec3f(0, 0, 0), dirV.GetNormalized(), yUp)

# Rotate XYZ.
rV = m.ExtractRotation().Decompose(Gf.Vec3d(0, 0, 1), Gf.Vec3d(0, 1, 0), Gf.Vec3d(1, 0, 0))
rV = Gf.Vec3d(rV[2], rV[1], rV[0])

print(f"rotateXYZ(Euler) : {rV}")


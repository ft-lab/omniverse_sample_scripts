from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, Sdf, Gf, Tf

translate = Gf.Vec3f(10.5, 2.8, 6.0)
rotation  = Gf.Quatf(0.7071, 0.7071, 0, 0)  # Gf.Rotation(Gf.Vec3d(1, 0, 0), 90)
scale     = Gf.Vec3f(2.0, 0.5, 1.0)

print("translate : " + str(translate))
print("rotation : " + str(rotation))
print("scale : " + str(scale))

# Make transform.
transM = UsdSkel.MakeTransform(translate, rotation, Gf.Vec3h(scale))
print("transform : " + str(transM))

# Decompose transform.
translate2, rotation2, scale2 = UsdSkel.DecomposeTransform(transM)
print("==> translate : " + str(translate2))
print("==> rotation : " + str(rotation2))
print("==> scale : " + str(scale2))

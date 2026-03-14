from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, Sdf, Gf, Tf

translate = Gf.Vec3f(10.5, 2.8, 6.0)
rotation  = Gf.Quatf(0.7071, 0.7071, 0, 0)  # Gf.Rotation(Gf.Vec3d(1, 0, 0), 90)
scale     = Gf.Vec3f(2.0, 0.5, 1.0)

print(f"translate : {translate}")
print(f"rotation : {rotation}")
print(f"scale : {scale}")
print("")

# --------------------------------------------------.
# Use UsdSkel.
# --------------------------------------------------.
# Make transform.
transM = UsdSkel.MakeTransform(translate, rotation, Gf.Vec3h(scale))
print(f"transform : {transM}")
print("")

# Decompose transform.
translate2, rotation2, scale2 = UsdSkel.DecomposeTransform(transM)
print(f"==> translate : {translate2}, type={type(translate2)}")
print(f"==> rotation : {rotation2}, type={type(rotation2)}")
print(f"==> scale : {scale2}, type={type(scale2)}")
print("")

# --------------------------------------------------.
# Use Gf.Matrix4d.
# --------------------------------------------------.
# Make transform with Gf.Matrix4d.
mTranslate = Gf.Matrix4d().SetTranslate(Gf.Vec3d(translate))
mRotate = Gf.Matrix4d().SetRotate(Gf.Quatd(rotation))
mScale = Gf.Matrix4d().SetScale(Gf.Vec3d(scale))
m = mScale * mRotate * mTranslate 
print(f"transform (Matrix4d) : {m}")
print("")


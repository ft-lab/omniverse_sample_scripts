from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

v1 = Gf.Vec3f(1.0, 2.0, -5.0)
v1N = v1.GetNormalized()
print(str(v1) + " ==> " + str(v1N))

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

v1 = Gf.Vec3f(1.0, 2.0, -5.0)
v2 = Gf.Vec3f(2.5, 14.0, 12.0)
print(f"{v1} : Length = {v1.GetLength()}")
print(f"{v2} : Length = {v2.GetLength()}")

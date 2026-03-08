from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

v1 = Gf.Vec3f(1.0, 2.0, -5.0)
v2 = Gf.Vec3f(2.5, 14.0, 12.0)

# Dot : Inner product.
print(f"{v1} x {v2} = {v1 * v2}")
print(f"{v1} x {v2} = {Gf.Dot(v1, v2)}")

# Cross : Outer product.
vx = v1[1] * v2[2] - v1[2] * v2[1]
vy = v1[2] * v2[0] - v1[0] * v2[2]
vz = v1[0] * v2[1] - v1[1] * v2[0]
print(f"Cross product : ( {vx}, {vy}, {vz} )")

cross = Gf.Cross(v1, v2)
print(f"Cross product : {cross}")

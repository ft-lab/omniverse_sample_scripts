from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# float vector.
print("\nfloat vector ----\n")
v1 = Gf.Vec3f(1.0, 2.0, -5.0)
v2 = Gf.Vec3f(2.5, 14.0, 12.0)

v = v1 + v2
print(f"{v1} + {v2} = {v}")

v = v1 / 2
print(f"{v1} / 2 = {v}")

print(f"v.x = {v[0]} type = {type(v[0])}")
print(f"v.y = {v[1]} type = {type(v[1])}")
print(f"v.z = {v[2]} type = {type(v[2])}")

# double vector.
# It seems to be internally converted to Gf.Vec3f.
print("\ndouble vector ----\n")
v1d = Gf.Vec3d(1.0, 2.0, -5.0)
v2d = Gf.Vec3d(2.5, 14.0, 12.0)

v = v1d + v2d
print("v.x = " + str(v1d[0]) + " type = " + str(type(v1d[0])))

v = v1d / 2
print(f"{v1d} / 2 = {v}")

print(f"v.x = {v[0]} type = {type(v[0])}")
print(f"v.y = {v[1]} type = {type(v[1])}")
print(f"v.z = {v[2]} type = {type(v[2])}")

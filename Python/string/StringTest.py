from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

v = 25.3674

print("Value = " + str(v))
print(f"Value = {v}")
print(f"Type = {type(v)}")

# Specify the number of decimal places.
# ==> "25.367"
print(f"Value = {'{:.3f}'.format(v)}")

vec3 = Gf.Vec3f(1.2, 5.6, 90)
print(f"vec3 = {vec3}")

array = [1.2, "test", True]
print(f"array = {array}")

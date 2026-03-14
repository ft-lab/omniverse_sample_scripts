from pxr import Gf

v1 = Gf.Vec3f(1.0, 2.0, -5.0)
v1N = v1.GetNormalized()
print(f"{v1} ==> {v1N}")

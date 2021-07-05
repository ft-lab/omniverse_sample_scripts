from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Identity matrix.
m = Gf.Matrix4f()
print(m)

# Initialize with rotation and translate.
rotV   = Gf.Rotation(Gf.Vec3d(1, 0, 0), 90.0)
transV = Gf.Vec3f(10, 5, 2.3)
m1 = Gf.Matrix4f(rotV, transV)
print(m1)

# Get data.
print (str(m1[0,0]) + " , " + str(m1[0,1]) + " , " + str(m1[0,2]) + " , " + str(m1[0,3]))
print (str(m1[1,0]) + " , " + str(m1[1,1]) + " , " + str(m1[1,2]) + " , " + str(m1[1,3]))
print (str(m1[2,0]) + " , " + str(m1[2,1]) + " , " + str(m1[2,2]) + " , " + str(m1[2,3]))
print (str(m1[3,0]) + " , " + str(m1[3,1]) + " , " + str(m1[3,2]) + " , " + str(m1[3,3]))

# Set identity.
m1.SetIdentity()
print(m1)

# Matrix multiplication.
rot1 = Gf.Rotation(Gf.Vec3d(1, 0, 0), 90.0)
m2 = Gf.Matrix4f(rot1, Gf.Vec3f())

rot2 = Gf.Rotation(Gf.Vec3d(0, 1, 0), 30.0)
m3 = Gf.Matrix4f(rot2, Gf.Vec3f())
m4 = m2 * m3
print(m4)

# Inverse matrix.
m4Inv = m4.GetInverse()
print(m4Inv)

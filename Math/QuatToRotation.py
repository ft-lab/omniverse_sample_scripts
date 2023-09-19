from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, Sdf, Gf, Tf

rotation = Gf.Quatf(0.7071, 0.7071, 0, 0)
print(f"quat : {rotation}")

# Convert from quaternion to Euler's rotation angles(degree).
# Rotate XYZ.
rot = Gf.Rotation(rotation)
rV = rot.Decompose(Gf.Vec3d(0, 0, 1), Gf.Vec3d(0, 1, 0), Gf.Vec3d(1, 0, 0))
rV = Gf.Vec3d(rV[2], rV[1], rV[0])
print(f"Euler's rotation angles : {rV}")

# RotationXYZ to quaternion.
rotX = Gf.Rotation(Gf.Vec3d(1, 0, 0), 90.0)
rotY = Gf.Rotation(Gf.Vec3d(0, 1, 0), 30.0)
rotZ = Gf.Rotation(Gf.Vec3d(0, 0, 1), -10.0)
rotXYZ = rotX * rotY * rotZ
q = rotXYZ.GetQuat()
print("quaternion : " + str(q))

# Quaternion to RotateXYZ.
rV = rotXYZ.Decompose(Gf.Vec3d(0, 0, 1), Gf.Vec3d(0, 1, 0), Gf.Vec3d(1, 0, 0))
rV = Gf.Vec3d(rV[2], rV[1], rV[0])
print(" Euler's rotation angles : " + str(rV))

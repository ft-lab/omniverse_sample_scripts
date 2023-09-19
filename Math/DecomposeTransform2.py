from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Dump matrix.
def DumpMatrix(m : Gf.Matrix4d):
    print("---------------------")
    for i in range(4):
        print(f"{mm[i,0]}  {mm[i,1]}  {mm[i,2]}  {mm[i,3]}")
    print("")

# Create Matrix4.
translate = Gf.Vec3d(10.5, 2.8, 6.0)
rotation  = Gf.Rotation(Gf.Vec3d(0, 1, 0), 20) * Gf.Rotation(Gf.Vec3d(0, 0, 1), 45)
scale     = Gf.Vec3d(2.0, 0.5, 1.0)

mm = Gf.Matrix4d().SetScale(scale) * Gf.Matrix4d(rotation, Gf.Vec3d(0)) * Gf.Matrix4d().SetTranslate(translate)
DumpMatrix(mm)

# Decompose matrix.
mm2 = mm.RemoveScaleShear()
rTrans = mm2.ExtractTranslation()
rRot = mm2.ExtractRotation()
mm3 = mm * mm2.GetInverse() 
rScale = Gf.Vec3d(mm3[0][0], mm3[1][1], mm3[2][2])

rAxisX = Gf.Vec3d(1, 0, 0)
rAxisY = Gf.Vec3d(0, 1, 0)
rAxisZ = Gf.Vec3d(0, 0, 1)
rRotE = rRot.Decompose(rAxisZ, rAxisY, rAxisX)
rRotE = Gf.Vec3d(rRotE[2], rRotE[1], rRotE[0])

print(f"Trans : {rTrans}")
print(f"Rot : {rRotE}")
print(f"Scale : {rScale}")


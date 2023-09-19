from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf
import omni.kit

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

xformCache = UsdGeom.XformCache(0)

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid():
        # Get world Transform.
        globalPose = xformCache.GetLocalToWorldTransform(prim)
        print(globalPose)

        # Decompose transform.
        translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

        # Conv Quat to eular angles.
        # Rotate XYZ.
        rV = Gf.Rotation(rotation).Decompose(Gf.Vec3d(0, 0, 1), Gf.Vec3d(0, 1, 0), Gf.Vec3d(1, 0, 0))
        rV = Gf.Vec3d(rV[2], rV[1], rV[0])

        print(f"==> translate : {translate}")
        print(f"==> rotation : {rV}")
        print(f"==> scale : {scale}")


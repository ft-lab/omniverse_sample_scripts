from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid():
        # Get world Transform.
        xformable = UsdGeom.Xformable(prim)
        globalPose = xformable.ComputeLocalToWorldTransform(0)
        print(globalPose)

        # Decompose transform.
        translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

        # Conv Quat to eular angles.
        rV = Gf.Rotation(rotation).Decompose(Gf.Vec3d(1, 0, 0), Gf.Vec3d(0, 1, 0), Gf.Vec3d(0, 0, 1))

        print("==> translate : " + str(translate))
        print("==> rotation : " + str(rV))
        print("==> scale : " + str(scale))


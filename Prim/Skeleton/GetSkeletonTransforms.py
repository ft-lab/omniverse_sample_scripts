from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf
import omni.kit

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

skel_cache = UsdSkel.Cache()
time_code = omni.timeline.get_timeline_interface().get_current_time() * stage.GetTimeCodesPerSecond()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() and prim.GetTypeName() == 'Skeleton':    
        # Get transform from cache.
        skel_query = skel_cache.GetSkelQuery(UsdSkel.Skeleton(prim))
        transforms = skel_query.ComputeJointLocalTransforms(time_code)

        # joints name.
        jointNames = skel_query.GetJointOrder()

        # joints matrix to translate, rotations, scales.
        translates, rotations, scales = UsdSkel.DecomposeTransforms(transforms)

        print(jointNames)
        print("  Translates : " + str(translates))
        print("  Rotations : " + str(rotations))
        print("  Scales : " + str(scales))



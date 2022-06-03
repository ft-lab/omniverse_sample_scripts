from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# -------------------------------------------------.
# Calculate bounding box in world coordinates.
# -------------------------------------------------.
def _calcWorldBoundingBox (prim : Usd.Prim):
    # Calc world boundingBox.
    bboxCache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), ["default"])
    bboxD = bboxCache.ComputeWorldBound(prim).ComputeAlignedRange()
    bb_min = Gf.Vec3f(bboxD.GetMin())
    bb_max = Gf.Vec3f(bboxD.GetMax())
    
    return bb_min, bb_max

# -------------------------------------------------.
for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue

    print("[ " + str(prim.GetName()) + "] ")
    bbMin, bbMax = _calcWorldBoundingBox(prim)
    print("  BoundingBox : " + str(bbMin) + " - " + str(bbMax))

    sx = bbMax[0] - bbMin[0]
    sy = bbMax[1] - bbMin[1]
    sz = bbMax[2] - bbMin[2]
    print("  BoundingBoxSize : " + str(sx) + " x " + str(sy) + " x " + str(sz))

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

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
# Calculate the distance between two selected shapes.
# -------------------------------------------------.
# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

wPosList = []
for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid():
        bbMin, bbMax = _calcWorldBoundingBox(prim)
        wCenter = Gf.Vec3f((bbMax[0] + bbMin[0]) * 0.5, (bbMax[1] + bbMin[1]) * 0.5, (bbMax[2] + bbMin[2]) * 0.5)
        wPosList.append(wCenter)
        continue

if len(wPosList) == 2:
    distV = (wPosList[1] - wPosList[0]).GetLength()
    print("Distance : " + str(distV) + " cm ( " + str(distV * 0.01) + " m)")


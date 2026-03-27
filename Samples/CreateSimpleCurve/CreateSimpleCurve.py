# ----------------------------------------------------------.
# SplineのCurveを作成するスクリプト.
# ----------------------------------------------------------.
from pxr import UsdGeom, UsdShade, UsdSkel, Gf
import numpy as np
import math
import omni.usd
import omni.ui

# Get stage.
stage = omni.usd.get_context().get_stage()

rootPath = "/World"

# --------------------------------------------------------.
# 3Dの頂点座標より、スプラインとして細分割した頂点を返す.
# @param[in] vList    Gf.Vec3fの配列.4つ以上であること.
# @param[in] divCou   分割数。len(vList)よりも大きい値のこと.
# @return 再分割されたGf.Vec3fの配列.
# --------------------------------------------------------.
def curveInterpolation(vList, divCou: int):
    pts = np.array([[p[0], p[1], p[2]] for p in vList], dtype=float)
    n = len(pts)
    if n == 0:
        return []
    if n == 1:
        return [Gf.Vec3f(*pts[0])] * divCou

    # 少ない点数は線形補間で扱う
    if n < 4:
        seg_lengths = np.linalg.norm(pts[1:] - pts[:-1], axis=1)
        total = seg_lengths.sum()
        if total == 0:
            return [Gf.Vec3f(*pts[0])] * divCou
        cum = np.concatenate(([0.0], np.cumsum(seg_lengths) / total))
        t_vals = np.linspace(0.0, 1.0, divCou)
        out = []
        for t in t_vals:
            i = np.searchsorted(cum, t, side='right') - 1
            i = min(max(i, 0), n - 2)
            local_denom = (cum[i+1] - cum[i]) if (cum[i+1] - cum[i]) > 0 else 1.0
            local_t = (t - cum[i]) / local_denom
            p = (1.0 - local_t) * pts[i] + local_t * pts[i+1]
            out.append(Gf.Vec3f(p[0], p[1], p[2]))
        return out

    # Catmull-Rom spline (各セグメントを均等分割してサンプル)
    segments = n - 1
    per_seg = int(np.ceil(divCou / segments))
    out_pts = []

    for i in range(segments):
        p0 = pts[i-1] if i-1 >= 0 else pts[0]
        p1 = pts[i]
        p2 = pts[i+1]
        p3 = pts[i+2] if (i+2) < n else pts[-1]

        if i < segments - 1:
            t = np.linspace(0.0, 1.0, per_seg, endpoint=False)
        else:
            t = np.linspace(0.0, 1.0, per_seg, endpoint=True)

        t2 = t * t
        t3 = t2 * t

        a = 0.5 * (2.0 * p1)
        b = 0.5 * (-p0 + p2)
        c = 0.5 * (2.0*p0 - 5.0*p1 + 4.0*p2 - p3)
        d = 0.5 * (-p0 + 3.0*p1 - 3.0*p2 + p3)

        seg_points = a[None, :] + np.outer(t, b) + np.outer(t2, c) + np.outer(t3, d)
        for rp in seg_points:
            out_pts.append(Gf.Vec3f(float(rp[0]), float(rp[1]), float(rp[2])))

    # 必要数に切り詰める／足りなければ最後の点で埋める
    if len(out_pts) >= divCou:
        return out_pts[:divCou]
    else:
        last = out_pts[-1]
        out_pts.extend([last] * (divCou - len(out_pts)))
        return out_pts

# --------------------------------------------------------.
# 選択Primの子で球の座標を配列に格納.
# @return Gf.Vec3fの配列, 半径(cm), マテリアル.
# --------------------------------------------------------.
def getSelectedSpheresPoint():
    selection = omni.usd.get_context().get_selection()
    paths = selection.get_selected_prim_paths()
    if len(paths) == 0:
        return None

    xformCache = UsdGeom.XformCache(0)
    prim = stage.GetPrimAtPath(paths[0])

    # retRに半径(cm)が入る。vPosList[]に頂点座標が入る.
    retR = -1.0
    vPosList = []
    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        if cPrim.IsA(UsdGeom.Sphere):
            globalPose = xformCache.GetLocalToWorldTransform(cPrim)

            # Decompose transform.
            translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

            # 半径を取得.
            if retR < 0.0:
                sphereGeom = UsdGeom.Sphere(cPrim)
                r = sphereGeom.GetRadiusAttr().Get()
                retR = r * scale[0]

            vPosList.append(translate)

    if len(vPosList) == 0:
        return None

    # primに割り当てられているマテリアルを取得.
    material = None
    rel = UsdShade.MaterialBindingAPI(prim).GetDirectBindingRel()
    pathList = rel.GetTargets()
    if len(pathList) > 0:
        materialPath = pathList[0]
        material = UsdShade.Material(stage.GetPrimAtPath(materialPath))

    return vPosList, retR, material

# --------------------------------------------------------.
# 外積の計算.
# --------------------------------------------------------.
def calcCross(v1 : Gf.Vec3f, v2 : Gf.Vec3f):
    return Gf.Cross(v1, v2)

# --------------------------------------------------------.
# 進行方向からベクトルを計算.
# @param[in]  vDir   進行方向のベクトル.
# @return 4x4行列.
# --------------------------------------------------------.
def calcDirToMatrix(vDir : Gf.Vec3f):
    vDir0 = vDir.GetNormalized()

    m  = Gf.Matrix4f()
    vX = Gf.Vec3f(1.0, 0.0, 0.0)
    vY = Gf.Vec3f(0.0, 1.0, 0.0)

    dirY = vY
    angleV = Gf.Dot(vDir0, vY)
    if math.fabs(angleV) > 0.999:
        dirY = vX
    dirX = calcCross(vDir0, dirY)
    dirX = dirX.GetNormalized()
    dirY = calcCross(dirX, vDir0)
    dirY = dirY.GetNormalized()

    m[0, 0] = dirX[0]
    m[0, 1] = dirX[1]
    m[0, 2] = dirX[2]
    m[1, 0] = dirY[0]
    m[1, 1] = dirY[1]
    m[1, 2] = dirY[2]
    m[2, 0] = vDir0[0]
    m[2, 1] = vDir0[1]
    m[2, 2] = vDir0[2]

    return m

# --------------------------------------------------------.
# 頂点の配列と半径、分割数により、チューブ状のMeshを作成.
# @param[in] name     形状名.
# @param[in] vList    Gf.Vec3fの配列.
# @param[in] radiusV  半径.
# @param[in] divUCou  円の分割数.
# @param[in] divVCou  進行方向での分割数.
# @param[in] material 割り当てるマテリアル.
# --------------------------------------------------------.
def createTubeMesh(name : str, vList, radiusV : float, divUCou : int, divVCou : int, material : UsdShade.Material):
    pathStr = f"{rootPath}/cables"

    prim = stage.GetPrimAtPath(pathStr)
    if not prim.IsValid():
        UsdGeom.Xform.Define(stage, pathStr)
        prim = stage.GetPrimAtPath(pathStr)

    # 子形状に同一名がある場合は連番を付ける.
    newName = name
    index = 0
    pChildren = prim.GetChildren()

    if pChildren != None:
        while True:
            chkF = False
            for cPrim in pChildren:
                name2 = cPrim.GetName()
                if name2 == newName:
                    index += 1
                    newName = f"{name}_{index}"
                    chkF = True
                    break
            
            if chkF == False:
                break

        name = newName

    meshName = f"{pathStr}/{name}"
    meshGeom = UsdGeom.Mesh.Define(stage, meshName)

    # Bind material.
    if material:
        UsdShade.MaterialBindingAPI(meshGeom).Bind(material)

    # +Zを中心とした半径radiusVのポイントを計算.
    circleV = []
    dd = (math.pi * 2.0) / ((float)(divUCou))
    dPos = 0.0
    for i in range(divUCou):
      circleV.append(Gf.Vec3f(math.cos(dPos), math.sin(dPos), 0.0))
      dPos += dd
    
    # ポリゴンメッシュのポイントと法線.
    m = Gf.Matrix4f()
    vDir0 = Gf.Vec3f(0.0, 0.0, 1.0)

    newVList  = []
    newVNList = []

    vListCou = len(vList)
    for i in range(vListCou):
        if i + 1 >= vListCou:
            p1 = vList[i]
        else:
            p1 = vList[i]
            p2 = vList[(i + 1) % vListCou]
            vDir = (p2 - p1).GetNormalized()

        if i == 0:
            m = calcDirToMatrix(p2 - p1)
            vDir0 = vDir
        else:
            mInv = m.GetInverse()
            pV0 = mInv.TransformDir(vDir0)
            pV1 = mInv.TransformDir(vDir)

            m0 = calcDirToMatrix(pV0)
            m1 = calcDirToMatrix(pV1)
            m = (m1.GetInverse() * m0).GetInverse() * m

        for j in range(divUCou):
            p = circleV[j]
            p = m.Transform(Gf.Vec3f(p[0] * radiusV, p[1] * radiusV, p[2] * radiusV))
            pp = p + p1
            newVList.append([pp[0], pp[1], pp[2]])
            pN = p.GetNormalized()
            newVNList.append([pN[0], pN[1], pN[2]])

        vDir0 = vDir

    meshGeom.CreatePointsAttr(newVList)
    meshGeom.CreateNormalsAttr(newVNList)

    # 面の頂点数の配列を格納.
    facesCou = (vListCou - 1) * divUCou
    faceVCouList = [int] * (facesCou)
    for i in range(facesCou):
        faceVCouList[i] = 4
    meshGeom.CreateFaceVertexCountsAttr(faceVCouList)

    # ポリゴンメッシュの面を配置.
    faceIndexList = []
    iPos = 0
    vCou = vListCou - 1
    for i in range(vCou):
        for j in range(divUCou):
            i0 = iPos + j
            i1 = iPos + ((j + 1) % divUCou)
            if i + 1 >= vListCou:
              i2 = ((j + 1) % divUCou)
              i3 = j
            else:
              i2 = iPos + divUCou + ((j + 1) % divUCou)
              i3 = iPos + divUCou + j

            faceIndexList.append(i3)
            faceIndexList.append(i2)
            faceIndexList.append(i1)
            faceIndexList.append(i0)

        iPos += divUCou

    meshGeom.CreateFaceVertexIndicesAttr(faceIndexList)

# ------------------------------------------.
# Clicked button event.
# ------------------------------------------.
def onButtonClick(hDivCouIntField):
    hDivCou = hDivCouIntField.model.get_value_as_int() 
    if hDivCou < 4:
        hDivCou = 4

    # 選択Primの子で球の座標を配列に格納.
    retV = getSelectedSpheresPoint()
    if retV is None:
        print("Select an XForm that contains spheres.")
    else:
        vPosList, retR, material = retV

        # 頂点座標の配置から、細分化した頂点を計算.
        newVPosList = curveInterpolation(vPosList, hDivCou)

        # チューブ形状を作成.
        createTubeMesh("cable", newVPosList, retR, 12, hDivCou, material)

# --------------------------------------------------------.
# メイン部.
# --------------------------------------------------------.
# ------------------------------------------.
# Create new window.
my_window = omni.ui.Window("Create Curve", width=300, height=200)

with my_window.frame:
    with omni.ui.VStack(height=0):
        hDivCouIntField = None

        with omni.ui.Placer(offset_x=8, offset_y=8):
            # Set label.
            f = omni.ui.Label("Select a Prim with multiple spheres as children.")

        with omni.ui.Placer(offset_x=8, offset_y=4):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Number of divisions : ", width=50)
                hDivCouIntField = omni.ui.IntField(width=200, height=0)
                hDivCouIntField.model.set_value(50)

        with omni.ui.Placer(offset_x=8, offset_y=4):
            # Set button.
            btn = omni.ui.Button("Create", width=200, height=0)
            btn.set_clicked_fn(lambda f = hDivCouIntField: onButtonClick(f))


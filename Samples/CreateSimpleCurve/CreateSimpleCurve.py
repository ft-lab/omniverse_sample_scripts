# ----------------------------------------------------------.
# SplineのCurveを作成するスクリプト.
# ----------------------------------------------------------.
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf
from scipy import interpolate
import numpy as np
import math
import omni.ui

# Get stage.
stage = omni.usd.get_context().get_stage()

rootPath = '/World'

# --------------------------------------------------------.
# 3Dの頂点座標より、スプラインとして細分割した頂点を返す.
# @param[in] vList    Gf.Vec3fの配列.4つ以上であること.
# @param[in] divCou   分割数。len(vList)よりも大きい値のこと.
# @return 再分割されたGf.Vec3fの配列.
# --------------------------------------------------------.
def curveInterpolation (vList, divCou : int):
    # XYZを配列に分離.
    xList = []
    yList = []
    zList = []
    for p in vList:
       xList.append(p[0])
       yList.append(p[1])
       zList.append(p[2])

    retVList = []

    tck,u = interpolate.splprep([xList, yList, zList], k=3, s=0)
    u = np.linspace(0, 1, num=divCou, endpoint=True) 
    spline = interpolate.splev(u, tck)

    for i in range(divCou):
        retVList.append(Gf.Vec3f(spline[0][i], spline[1][i], spline[2][i]))

    return retVList

# --------------------------------------------------------.
# 選択Primの子で球の座標を配列に格納.
# @return Gf.Vec3fの配列, 半径(cm), マテリアル.
# --------------------------------------------------------.
def getSelectedSpheresPoint ():
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
        typeName = cPrim.GetTypeName()
        if typeName == 'Sphere':
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
def calcCross (v1 : Gf.Vec3f, v2 : Gf.Vec3f):
    v1_2 = Gf.Vec4f(v1[0], v1[1], v1[2], 1.0)
    v2_2 = Gf.Vec4f(v2[0], v2[1], v2[2], 1.0)

    v3 = Gf.HomogeneousCross(v1_2, v2_2)
    return Gf.Vec3f(v3[0], v3[1], v3[2])

# --------------------------------------------------------.
# 進行方向からベクトルを計算.
# @param[in]  vDir   進行方向のベクトル.
# @return 4x4行列.
# --------------------------------------------------------.
def calcDirToMatrix (vDir : Gf.Vec3f):
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
def createTubeMesh (name : str, vList, radiusV : float, divUCou : int, divVCou : int, material : UsdShade.Material):
    pathStr = rootPath + '/cables'

    prim = stage.GetPrimAtPath(pathStr)
    if prim.IsValid() == False:
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
                    newName = name + '_' + str(index)
                    chkF = True
                    break
            
            if chkF == False:
                break

        name = newName

    meshName = pathStr + '/' + name
    meshGeom = UsdGeom.Mesh.Define(stage, meshName)

    # Bind material.
    if material != None:
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
    if retV == None:
        print("Select an XForm that contains spheres.")
    else:
        vPosList, retR, material = retV

        # 頂点座標の配置から、細分化した頂点を計算.
        newVPosList = curveInterpolation(vPosList, hDivCou)

        # チューブ形状を作成.
        createTubeMesh('cable', newVPosList, retR, 12, hDivCou, material)

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


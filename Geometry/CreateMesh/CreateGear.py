from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import math
import omni.ui

# Get stage.
stage = omni.usd.get_context().get_stage()

# -------------------------------------------------------.
# Calculate normal.
# -------------------------------------------------------.
def calcTriangleNormal (v1 : Gf.Vec3d, v2 : Gf.Vec3d, v3 : Gf.Vec3d):
    e1 = v2 - v1
    e2 = v3 - v2
    e1 = Gf.Vec4f(e1[0], e1[1], e1[2],1.0)
    e2 = Gf.Vec4f(e2[0], e2[1], e2[2],1.0)
    e3 = Gf.HomogeneousCross(e1, e2)

    n = Gf.Vec3d(e3[0], e3[1], e3[2])
    return n.GetNormalized()

# -------------------------------------------------------.
# Attach thickness.
# @param[in] primPath    Target Prim path.
# @param[in] thickness   Thickness.
# -------------------------------------------------------.
def AttachThickness (primPath : str, thickness : float):
    prim = stage.GetPrimAtPath(primPath)
    if prim.IsValid() == False:
        return
    
    if prim.GetTypeName() != 'Mesh':
        return

    m = UsdGeom.Mesh(prim)

    # Number of faces.
    faceVCouList = m.GetFaceVertexCountsAttr().Get()
    faceCou = len(faceVCouList)
    if faceCou == 0:
        return

    normalsList = m.GetNormalsAttr().Get()
    normalsCou = len(normalsList)
    if normalsCou == 0:
        return
    normalV = normalsList[0]

    versList = m.GetPointsAttr().Get()
    versCou = len(versList)
    if versCou < 3:
        return

    faceVIList = m.GetFaceVertexIndicesAttr().Get()
    faceVICou = len(faceVIList)

    # Stores the face number for each vertex.
    vFList = [[]] * (versCou)
    for i in range(versCou):
        vFList[i] = []
    index = 0
    for i in range(len(faceVCouList)):
        faceVCou = faceVCouList[i]
        for j in range(faceVCou):
            vI = faceVIList[index + j]
            vFList[vI].append(i)            
        index += faceVCou

    faceIndicesList = [[]] * faceCou
    for i in range(faceCou):
        faceIndicesList[i] = []
    
    # Rearrange the vertex indices per face.
    index = 0
    for i in range(faceCou):
        faceVCou = faceVCouList[i]
        for j in range(faceVCou):
            faceIndicesList[i].append(faceVIList[index + j])
        index += faceVCou

    # Create a list of independent edges.
    edgesList = []
    for i in range(faceCou):
        faceVCou = faceVCouList[i]
        for j in range(faceVCou):
            vI1 = faceIndicesList[i][j]
            vI2 = faceIndicesList[i][(j + 1) % faceVCou]
            
            chkF = False
            cI = -1
            for k in range(len(edgesList)):
                if (edgesList[k][0] == vI1 and edgesList[k][1] == vI2) or (edgesList[k][0] == vI2 and edgesList[k][1] == vI1):
                    chkF = True
                    cI = k
                    break
            if chkF == False:
                edgesList.append([vI1, vI2, 1])
            else:
                cou = edgesList[cI][2]
                edgesList[cI] = [vI1, vI2, cou + 1]

    edgesOneList = []
    for p in edgesList:
        if p[2] == 1:
            edgesOneList.append([p[0], p[1]])

    # Create a symmetrical face.
    faceVCouList2 = [0] * (faceCou * 2)
    normalsList2  = [(0.0, 0.0, 0.0)] * (normalsCou * 2)
    versList2     = [(0.0, 0.0, 0.0)] * (versCou * 2)
    faceVIList2   = [0] * (faceVICou * 2)

    for i in range(faceCou):
        faceVCouList2[i] = faceVCouList[i]
        faceVCouList2[i + faceCou] = faceVCouList[i]

    for i in range(faceVICou):
        faceVIList2[i] = faceVIList[i]
        faceVIList2[i + faceVICou] = faceVIList[faceVICou - i - 1] + versCou

    for i in range(normalsCou):
        normalsList2[i] = normalsList[i]
        normalsList2[i + normalsCou] = -normalsList[i]

    for i in range(versCou):
        versList2[i] = versList[i]
        n = normalsList[i]
        versList2[i + versCou] = versList[i] - (n * thickness)

    # Create side faces.
    vIndex = len(versList2)
    for edgeI in edgesOneList:
        e1 = edgeI[0]
        e2 = edgeI[1]
        i1 = e1
        i2 = e2
        i3 = e1 + versCou
        i4 = e2 + versCou
        v1 = versList2[i2]
        v2 = versList2[i1]
        v3 = versList2[i3]
        v4 = versList2[i4]
        n = calcTriangleNormal(v1, v2, v3)

        faceVCouList2.append(4)
        for j in range(4):
            normalsList2.append(n)
        versList2.append(v1)
        versList2.append(v2)
        versList2.append(v3)
        versList2.append(v4)
        for j in range(4):
            faceVIList2.append(vIndex + j)

        vIndex += 4
    
    m.CreatePointsAttr(versList2)
    m.CreateNormalsAttr(normalsList2)
    m.CreateFaceVertexCountsAttr(faceVCouList2)
    m.CreateFaceVertexIndicesAttr(faceVIList2)

# -------------------------------------------------------.
# Create gear.
# @param[in] name          Prim name.
# @param[in] gearR         Radius of gear.
# @param[in] filletCount   Number of gear divisions.
# @param[in] filletHeight  Fillet height.
# @param[in] gearWidth     Gear width.
# -------------------------------------------------------.
def CreateGear (name : str, gearR : float, filletCount : int, filletHeight : float, gearWidth : float):
    angle = 360.0 / filletCount  # Angle of one tooth.

    # Calculate the length of one tooth on the circumference.
    D = (gearR * math.sin((angle / 2.0) * math.pi / 180.0)) * 2
    dHalf    = D * 0.5
    dQuarter = D * 0.25

    centerV = Gf.Vec3d(0, 0, 0)

    versList = []
    versList.append(centerV)
    faceIndexList = []

    maxVCou = 1 + (5 * filletCount)

    index = 1
    aV = 0.0
    for i in range(filletCount):
        # Vertices of a single tooth.
        vDirX = math.cos(aV * math.pi / 180.0)
        vDirY = math.sin(aV * math.pi / 180.0)
        v2X = -vDirY
        v2Y =  vDirX

        vD      = Gf.Vec3d(vDirX, vDirY, 0)
        vCrossD = Gf.Vec3d(v2X, v2Y, 0)
        vCenter = vD * gearR
        v1 = vCenter - (vCrossD * dHalf)
        v2 = v1 + (vCrossD * dQuarter)
        v3 = v2 + (vD * filletHeight)
        v4 = v3 + (vCrossD * dHalf)
        v5 = v4 - (vD * filletHeight)
        v6 = v5 + (vCrossD * dQuarter)

        dd = D * 0.1
        vCD = vCrossD * dd
        v3 += vCD
        v4 -= vCD
        v2 -= vCD
        v5 += vCD

        versList.append(v1)
        versList.append(v2)
        versList.append(v3)
        versList.append(v4)
        versList.append(v5)

        faceIndexList.append(0)
        faceIndexList.append(index)
        faceIndexList.append(index + 1)
        faceIndexList.append(index + 2)
        faceIndexList.append(index + 3)
        faceIndexList.append(index + 4)
        if index + 5 >= maxVCou:
            faceIndexList.append(1)
        else:
            faceIndexList.append(index + 5)

        index += 5

        aV += angle

    # Get default prim.
    defaultPrim = stage.GetDefaultPrim()

    # Get root path.
    rootPath = '/'
    if defaultPrim.IsValid():
        rootPath = defaultPrim.GetPath().pathString

    # Create mesh.
    pathName = rootPath + '/gears'
    prim = stage.GetPrimAtPath(pathName)
    if prim.IsValid() == False:
        UsdGeom.Xform.Define(stage, pathName)

    pathMeshName0 = pathName + '/' + name
    pathMeshName = pathMeshName0
    index = 0
    while True:
        pathMeshName = pathMeshName0
        if index > 0:
            pathMeshName += '_' + str(index)
        prim = stage.GetPrimAtPath(pathMeshName)
        if prim.IsValid() == False:
            break
        index += 1

    meshGeom = UsdGeom.Mesh.Define(stage, pathMeshName)

    # Set vertices.
    stVersList = []
    stNormalList = []
    for i in range(len(versList)):
        stVersList.append((versList[i][0], versList[i][1], versList[i][2]))
        stNormalList.append((0, 0, 1))
    meshGeom.CreatePointsAttr(stVersList)

    # Set normals.
    meshGeom.CreateNormalsAttr(stNormalList)

    # Set face vertex count.
    faceVCouList = []
    for i in range(filletCount):
        faceVCouList.append(7)
    meshGeom.CreateFaceVertexCountsAttr(faceVCouList)

    # Set face vertex indices.
    meshGeom.CreateFaceVertexIndicesAttr(faceIndexList)

    # Set position.
    UsdGeom.XformCommonAPI(meshGeom).SetTranslate((0.0, 0.0, 0.0))

    # Set rotation.
    UsdGeom.XformCommonAPI(meshGeom).SetRotate((0.0, 0.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

    # Set scale.
    UsdGeom.XformCommonAPI(meshGeom).SetScale((1.0, 1.0, 1.0))

    # Attach thickness.
    if gearWidth > 0.0:
        AttachThickness(pathMeshName, gearWidth)

# --------------------------------------------------------.
# Main UI.
# --------------------------------------------------------.
# Clicked button event.
def onButtonClick (hNameStringField, hRadiusFloatField, hFilletCouIntField, hFilletHeightFloatField, hGearWidthFloatField):
    name = hNameStringField.model.get_value_as_string()
    if name == '':
        name = 'gear'

    radius = hRadiusFloatField.model.get_value_as_float() 
    if radius < 0.00001:
        radius = 0.00001

    filletCou = hFilletCouIntField.model.get_value_as_int() 
    if filletCou < 4:
        filletCou = 4

    filletHeight = hFilletHeightFloatField.model.get_value_as_float() 
    if filletHeight < 0.00001:
        filletHeight = 0.00001

    gearWidth = hGearWidthFloatField.model.get_value_as_float() 
    if gearWidth < 0.00001:
        gearWidth = 0.00001

    # Create Cear.
    CreateGear(name, radius, filletCou, filletHeight, gearWidth)

# ------------------------------------------.
my_window = omni.ui.Window("Create Gear", width=350, height=250)

with my_window.frame:
    with omni.ui.VStack(height=0):
        labelWidth = 120
        
        with omni.ui.Placer(offset_x=8, offset_y=8):
            # Set label.
            f = omni.ui.Label("Create Gear.")

        with omni.ui.Placer(offset_x=8, offset_y=4):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Name : ", width=labelWidth)
                hNameStringField = omni.ui.StringField(width=200, height=0)
                hNameStringField.model.set_value("gear")

        with omni.ui.Placer(offset_x=8, offset_y=4):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Radius : ", width=labelWidth)
                hRadiusFloatField = omni.ui.FloatField(width=200, height=0)
                hRadiusFloatField.model.set_value(10.0)

        with omni.ui.Placer(offset_x=8, offset_y=4):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Number of fillet : ", width=labelWidth)
                hFilletCouIntField = omni.ui.IntField(width=200, height=0)
                hFilletCouIntField.model.set_value(32)

        with omni.ui.Placer(offset_x=8, offset_y=4):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Fillet height : ", width=labelWidth)
                hFilletHeightFloatField = omni.ui.FloatField(width=200, height=0)
                hFilletHeightFloatField.model.set_value(1.0)

        with omni.ui.Placer(offset_x=8, offset_y=4):
            with omni.ui.HStack(width=300):
                omni.ui.Label("Gear width : ", width=labelWidth)
                hGearWidthFloatField = omni.ui.FloatField(width=200, height=0)
                hGearWidthFloatField.model.set_value(2.0)

        with omni.ui.Placer(offset_x=8, offset_y=4):
            # Set button.
            btn = omni.ui.Button("Create", width=200, height=0)
            btn.set_clicked_fn(lambda name = hNameStringField, f = hRadiusFloatField, f2 = hFilletCouIntField, f3 = hFilletHeightFloatField, f4 = hGearWidthFloatField: onButtonClick(name, f, f2, f3, f4))


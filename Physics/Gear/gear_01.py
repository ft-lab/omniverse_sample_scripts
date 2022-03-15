from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf, UsdSkel, PhysxSchema
import math

# Get stage.
g_stage = omni.usd.get_context().get_stage()

# gear path.
gear_basePath = '/World/gears'

# Y-Up.
UsdGeom.SetStageUpAxis(g_stage, UsdGeom.Tokens.y)

xformCache = UsdGeom.XformCache(0)

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
    prim = g_stage.GetPrimAtPath(primPath)
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
# @param[in] position      position.
# -------------------------------------------------------.
def CreateGear (name : str, gearR : float, filletCount : int, filletHeight : float, gearWidth : float, position : Gf.Vec3f):
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

    # Create mesh.
    pathName = "/World/gears"
    prim = g_stage.GetPrimAtPath(pathName)
    if prim.IsValid() == False:
        UsdGeom.Xform.Define(g_stage, pathName)

    pathMeshName0 = pathName + '/' + name
    pathMeshName = pathMeshName0
    index = 0
    while True:
        pathMeshName = pathMeshName0
        if index > 0:
            pathMeshName += '_' + str(index)
        prim = g_stage.GetPrimAtPath(pathMeshName)
        if prim.IsValid() == False:
            break
        index += 1

    meshGeom = UsdGeom.Mesh.Define(g_stage, pathMeshName)

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
    UsdGeom.XformCommonAPI(meshGeom).SetTranslate((position[0], position[1], position[2]))

    # Set rotation.
    UsdGeom.XformCommonAPI(meshGeom).SetRotate((0.0, 0.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

    # Set scale.
    UsdGeom.XformCommonAPI(meshGeom).SetScale((1.0, 1.0, 1.0))

    # Attach thickness.
    if gearWidth > 0.0:
        AttachThickness(pathMeshName, gearWidth)

# ------------------------------------------
# Get prim center position.
# @param[in] primPath   Prim path.
# @return  position(Gf.Vec3f)
# ------------------------------------------
def GetPrimCenter (primPath : str):
    prim = g_stage.GetPrimAtPath(primPath)
    if prim.IsValid() == False:
        return
    
    globalPose = xformCache.GetLocalToWorldTransform(prim)
    translate, rotation, scale = UsdSkel.DecomposeTransform(globalPose)

    return translate

# ------------------------------------------
# Set RigidBody on gear.
# ------------------------------------------
def SetRigidBodyOnGear (primPath : str, index : int):
    prim = g_stage.GetPrimAtPath(primPath)
    if prim.IsValid() == False:
        return

    physicsAPI = UsdPhysics.RigidBodyAPI.Apply(prim)
    UsdPhysics.MassAPI.Apply(prim)

    UsdPhysics.CollisionAPI.Apply(prim)

    pos = GetPrimCenter(primPath)

    # revolute joint
    path = gear_basePath + '/revoluteJoint_' + str(index)
    revoluteJoint = UsdPhysics.RevoluteJoint.Define(g_stage, path)
    revoluteJoint.CreateAxisAttr("Z")
    revoluteJoint.CreateBody1Rel().SetTargets([primPath])
    revoluteJoint.CreateLocalPos0Attr().Set(pos)        
    revoluteJoint.CreateLocalRot0Attr().Set(Gf.Quatf(1.0))

    revoluteJoint.CreateLocalPos1Attr().Set(Gf.Vec3f(0.0, 0.0, 0.0))
    revoluteJoint.CreateLocalRot1Attr().Set(Gf.Quatf(1.0))

# -----------------------------------------------

# Radius.
radius1 = 5.0
radius2 = 10.0
radius3 = 6.25

# Create Gears.
CreateGear("gear", radius1, 24, 1.0, 1.0, Gf.Vec3f(0, 0, 0))
CreateGear("gear_1", radius2, 48, 1.0, 1.0, Gf.Vec3f(16.3, 0.72, 0))
CreateGear("gear_2", radius3, 30, 1.0, 1.0, Gf.Vec3f(0.0, -12.6, 0))

# gear1 path.
gear1_path = gear_basePath + '/gear'

# gear2 path.
gear2_path = gear_basePath + '/gear_1'

# gear3 path.
gear3_path = gear_basePath + '/gear_2'

# Physics scene definition.
scene = UsdPhysics.Scene.Define(g_stage, "/physicsScene")
scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, -1.0, 0.0))
scene.CreateGravityMagnitudeAttr().Set(981.0)

gear1_prim = g_stage.GetPrimAtPath(gear1_path)

pos1 = GetPrimCenter(gear1_path)

# Set RigidBody on gear.
SetRigidBodyOnGear(gear1_path, 0)
SetRigidBodyOnGear(gear2_path, 1)
SetRigidBodyOnGear(gear3_path, 2)

# add angular drive.
revolute0_path = gear_basePath + "/revoluteJoint_0"
revolute1_path = gear_basePath + "/revoluteJoint_1"
revolute2_path = gear_basePath + "/revoluteJoint_2"

# gear joint (0-1)
gearJoint = PhysxSchema.PhysxPhysicsGearJoint.Define(g_stage, "/gearJoint_0_1")

gearJoint.CreateBody0Rel().SetTargets([gear1_path])
gearJoint.CreateBody1Rel().SetTargets([gear2_path])

gearJoint.CreateGearRatioAttr(radius1/radius2)
gearJoint.CreateHinge0Rel().SetTargets([revolute0_path])
gearJoint.CreateHinge1Rel().SetTargets([revolute1_path])

# gear joint (0-2)
gearJoint2 = PhysxSchema.PhysxPhysicsGearJoint.Define(g_stage, "/gearJoint_0_2")

gearJoint2.CreateBody0Rel().SetTargets([gear1_path])
gearJoint2.CreateBody1Rel().SetTargets([gear3_path])

gearJoint2.CreateGearRatioAttr(radius1/radius3)
gearJoint2.CreateHinge0Rel().SetTargets([revolute0_path])
gearJoint2.CreateHinge1Rel().SetTargets([revolute2_path])

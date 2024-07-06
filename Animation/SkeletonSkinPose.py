from pxr import Usd, UsdGeom, UsdPhysics, UsdSkel, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# --------------------------------------------.
# Create mesh.
# @pram[in] primPath  Prim path.
# @pram[in] height    height of mesh.
# @pram[in] divCou    Number of height divisions.
# @return UsdGeom.Mesh
# --------------------------------------------.
def createMesh(primPath : str, height : float = 100.0, divCou : int = 8):
    meshGeom = UsdGeom.Mesh.Define(stage, primPath)

    pointsA = []
    dV = height / float(divCou)
    py = 0.0
    for i in range(divCou + 1):
        pointsA.append((-10.0, py, 0.0))
        pointsA.append(( 10.0, py, 0.0))
        py += dV
    meshGeom.CreatePointsAttr(pointsA)

    normalsA = []
    for i in range(divCou + 1):
        normalsA.append((0.0, 0.0, 1.0))
        normalsA.append((0.0, 0.0, 1.0))
    meshGeom.CreateNormalsAttr(normalsA)
    meshGeom.SetNormalsInterpolation("vertex")

    meshGeom.CreateFaceVertexCountsAttr([4] * divCou)

    faceVertexIndicesA = []
    iV = 0
    for i in range(divCou):
        faceVertexIndicesA.append(iV + 0)
        faceVertexIndicesA.append(iV + 1)
        faceVertexIndicesA.append(iV + 3)
        faceVertexIndicesA.append(iV + 2)
        iV += 2
    meshGeom.CreateFaceVertexIndicesAttr(faceVertexIndicesA)

    dV = 1.0 / float(divCou)
    uvsA = []
    v = 0.0
    for i in range(divCou + 1):
        uvsA.append((0.0, v))
        uvsA.append((1.0, v))
        v += dV

    primvarV = UsdGeom.PrimvarsAPI(meshGeom).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.vertex)
    attr = primvarV.GetAttr()
    attr.Set(uvsA)

    boundable = UsdGeom.Boundable(meshGeom.GetPrim())
    extent = boundable.ComputeExtent(Usd.TimeCode(0))

    meshGeom.CreateExtentAttr(extent)
    meshGeom.CreateSubdivisionSchemeAttr().Set("none")

    return meshGeom

# --------------------------------------------.
# Create mesh with skeleton and skin.
# @pram[in] primPath  Prim path.
# @pram[in] height    height of mesh.
# @pram[in] divCou    Number of height divisions.
# --------------------------------------------.
def createMeshWithSkeletonSkin(primPath : str, height : float = 100.0, divCou : int = 8):
    # Create SkelRoot.
    skelRoot = UsdSkel.Root.Define(stage, primPath)
    skelRootPrim = skelRoot.GetPrim()

    # Create Skeleton.
    skeleton = UsdSkel.Skeleton.Define(stage, f"{primPath}/skeleton")
    skeletonPrim = skeleton.GetPrim()

    # Create mesh.
    meshGeom = createMesh(f"{primPath}/mesh", height, divCou)
    prim = meshGeom.GetPrim()

    # -----------------------------------------------------------.
    # Create joints.
    # joints = ["root", "root/bone1", "root/bone1/bone2", "root/bone1/bone2/bone3"]
    joints = []
    bindTransforms = []
    restTransforms = []

    jointName = "root"
    joints.append(jointName)

    bindTransform = Gf.Matrix4d(Gf.Rotation(), Gf.Vec3d(0, 0, 0))
    restTransform = Gf.Matrix4d(Gf.Rotation(), Gf.Vec3d(0, 0, 0))
    bindTransforms.append(bindTransform)
    restTransforms.append(restTransform)

    baseTransform = restTransform

    # Bones spaced 2 points apart.
    bonesCou = int(divCou / 2)
    boneDY = height / float(bonesCou)
    py = boneDY
    for i in range(bonesCou):
        jointName = f"{jointName}/bone{i + 1}"
        joints.append(jointName)

        wTransform = Gf.Matrix4d(Gf.Rotation(), Gf.Vec3d(0.0, py, 0.0))
        bindTransform = wTransform
        restTransform = (bindTransforms[-1].GetInverse() * wTransform)
        bindTransforms.append(bindTransform)
        restTransforms.append(restTransform)
        py += boneDY

    skeleton.CreateJointsAttr().Set(joints)
    skeleton.CreateBindTransformsAttr().Set(bindTransforms)
    skeleton.CreateRestTransformsAttr().Set(restTransforms)

    # -----------------------------------------------------------.
    # Set skin weights in mesh.
    jointIndices = []
    jointWeights = []
    elementSize = 2
    boneIndex = 0
    for i in range(divCou + 1):
        for j in range(2):
            if not (i & 1):
                jointIndices.append(boneIndex)
                jointWeights.append(1.0)
                jointIndices.append(0)
                jointWeights.append(0.0)
            else:
                jointIndices.append(boneIndex)
                jointWeights.append(0.8)
                jointIndices.append(boneIndex + 1)
                jointWeights.append(0.2)
        if i & 1:
            boneIndex += 1

    primvarsAPI = UsdGeom.PrimvarsAPI(prim)
    primvarsAPI.CreatePrimvar("skel:jointIndices", Sdf.ValueTypeNames.IntArray, UsdGeom.Tokens.vertex, elementSize).Set(jointIndices)
    primvarsAPI.CreatePrimvar("skel:jointWeights", Sdf.ValueTypeNames.FloatArray, UsdGeom.Tokens.vertex, elementSize).Set(jointWeights)

    # Assign skeleton.
    bindingAPI = UsdSkel.BindingAPI(prim)
    bindingAPI.CreateSkeletonRel().SetTargets([skeleton.GetPath()])
    bindingAPI.Apply(prim)

# --------------------------------------------.
# Create skelAnimation.
# @pram[in] skeletonPrim  Skeleton prim path.
def createSkelAnimation(skeletonPrimPath : str):
    skeletonPrim = stage.GetPrimAtPath(skeletonPrimPath)
    if not skeletonPrim.IsValid():
        return

    primPath = f"{skeletonPrimPath}/skelAnim"
    skelAnim = stage.GetPrimAtPath(primPath)
    if not skelAnim.IsValid():
        skelAnim = UsdSkel.Animation.Define(stage, primPath)
    else:
        skelAnim = UsdSkel.Animation(skelAnim)
    
    # Set SkelAnim.
    UsdSkel.BindingAPI(skeletonPrim).CreateAnimationSourceRel().SetTargets([skelAnim.GetPath()])
    UsdSkel.BindingAPI.Apply(skeletonPrim)

    return skelAnim

# --------------------------------------------.
# Convert RotationXYZ to QuatF.
# @param[in] rotXYZ  Euler angles (XYZ).
# @return  Quaternion.
def convertRotationXYZToQuatF(rotXYZ : Gf.Vec3f):
    rotX = Gf.Rotation(Gf.Vec3d(1, 0, 0), rotXYZ[0])
    rotY = Gf.Rotation(Gf.Vec3d(0, 1, 0), rotXYZ[1])
    rotZ = Gf.Rotation(Gf.Vec3d(0, 0, 1), rotXYZ[2])
    rotXYZ = rotX * rotY * rotZ
    q = rotXYZ.GetQuat()
    return Gf.Quatf(q)

# --------------------------------------------.
# Convert QuatF to RotationXYZ.
def convertQuatFToRotationXYZ(quat):
    rV = Gf.Rotation(quat).Decompose(Gf.Vec3d(0, 0, 1), Gf.Vec3d(0, 1, 0), Gf.Vec3d(1, 0, 0))
    rV = Gf.Vec3d(rV[2], rV[1], rV[0])
    return rV

# --------------------------------------------------------.

# Create target skeleton.
# This is the same process as "SkeletonSkin.py".
primPath = "/World/skeletonTest"
divCou = 8
height = 100.0
createMeshWithSkeletonSkin(primPath, height, divCou)

# Create skelAnimation.
skeletonPrimPath = f"{primPath}/skeleton"
skelAnim = createSkelAnimation(skeletonPrimPath)

# Get Skeleton.
skeletonPrim = stage.GetPrimAtPath(skeletonPrimPath)
skeleton = UsdSkel.Skeleton(skeletonPrim)

# Get Joint names list.
jointNamesList = skeleton.GetJointsAttr().Get()
print(jointNamesList)

# Rest transform list.
# Get the local coordinate values ​​for Translation, Rotation, and Scale from here.
translationList = []
rotationList = []
scaleList = []
restTransforms = skeleton.GetRestTransformsAttr().Get()
for m in restTransforms:
    # Decompose Transform into Translate, Rotate, and Scale.
    translation, rotation, scale = UsdSkel.DecomposeTransform(m)

    translationList.append(Gf.Vec3f(translation))
    rotationList.append(Gf.Quatf(rotation))
    scaleList.append(Gf.Vec3f(scale))

rotationList[1] = convertRotationXYZToQuatF(Gf.Vec3f(-30.0, 0.0, 0.0))
rotationList[2] = convertRotationXYZToQuatF(Gf.Vec3f(-20.0, 0.0, 0.0))

# Store a list of Joint names in SkelAnimation.
jointsAttr = skelAnim.CreateJointsAttr()
jointsAttr.Set(jointNamesList)

# Clear cache.
xformCache = UsdGeom.XformCache()
xformCache.Clear()

attr = skelAnim.CreateTranslationsAttr()
attr.Set(translationList)

attr = skelAnim.GetRotationsAttr()
attr.Set(rotationList)

attr = skelAnim.CreateScalesAttr()
attr.Set(scaleList)


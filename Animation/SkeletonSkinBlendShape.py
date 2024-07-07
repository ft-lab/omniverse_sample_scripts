from pxr import Usd, UsdGeom, UsdPhysics, UsdSkel, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# --------------------------------------------.
# Create Plane mesh.
# @pram[in] primPath  Prim path.
# @pram[in] planeSize size.
# --------------------------------------------.
def createPlaneMesh (meshPath : str, planeSize : float = 20.0):
    # Create mesh.
    meshGeom = UsdGeom.Mesh.Define(stage, meshPath)

    # Set vertices.
    planeSizeH = planeSize * 0.5
    meshGeom.CreatePointsAttr([(-planeSizeH, 0, planeSizeH), (planeSizeH, 0, planeSizeH), (planeSizeH, 0, -planeSizeH), (-planeSizeH, 0, -planeSizeH)])

    # Set face vertex count.
    meshGeom.CreateFaceVertexCountsAttr([4])

    # Set face vertex indices.
    meshGeom.CreateFaceVertexIndicesAttr([0, 1, 2, 3])

    # Set normals.
    normalList = [(0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0)]
    meshGeom.CreateNormalsAttr(normalList)
    meshGeom.SetNormalsInterpolation("faceVarying")

    # Set uvs.
    primvarV = UsdGeom.PrimvarsAPI(meshGeom).CreatePrimvar("st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying)
    attr = primvarV.GetAttr()

    uvsList = [(0.0, 1.0), (0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    attr.Set(uvsList)

    # Subdivision is set to none.
    meshGeom.CreateSubdivisionSchemeAttr().Set("none")

    # Set position.
    UsdGeom.XformCommonAPI(meshGeom).SetTranslate((0.0, 0.0, 0.0))

    # Set rotation.
    UsdGeom.XformCommonAPI(meshGeom).SetRotate((0.0, 0.0, 0.0), UsdGeom.XformCommonAPI.RotationOrderXYZ)

    # Set scale.
    UsdGeom.XformCommonAPI(meshGeom).SetScale((1.0, 1.0, 1.0))

    return meshGeom

# --------------------------------------------.
# Create Plane mesh with skeleton.
# @pram[in] primPath  Prim path.
# @pram[in] planeSize size.
# --------------------------------------------.
def createPlaneMeshWithSkeletonSkin(primPath : str, planeSize : float = 100.0):
    # Create SkelRoot.
    skelRoot = UsdSkel.Root.Define(stage, primPath)
    skelRootPrim = skelRoot.GetPrim()

    # Create Skeleton.
    skeleton = UsdSkel.Skeleton.Define(stage, f"{primPath}/skeleton")
    skeletonPrim = skeleton.GetPrim()

    # Create mesh.
    meshGeom = createPlaneMesh(f"{primPath}/mesh", planeSize)
    prim = meshGeom.GetPrim()

    # -----------------------------------------------------------.
    # Create joints.
    # joints = ["root"]
    joints = []
    bindTransforms = []
    restTransforms = []

    jointName = "root"
    joints.append(jointName)

    bindTransform = Gf.Matrix4d(Gf.Rotation(), Gf.Vec3d(0, 0, 0))
    restTransform = Gf.Matrix4d(Gf.Rotation(), Gf.Vec3d(0, 0, 0))
    bindTransforms.append(bindTransform)
    restTransforms.append(restTransform)

    skeleton.CreateJointsAttr().Set(joints)
    skeleton.CreateBindTransformsAttr().Set(bindTransforms)
    skeleton.CreateRestTransformsAttr().Set(restTransforms)

    # Assign skeleton.
    bindingAPI = UsdSkel.BindingAPI(prim)
    bindingAPI.CreateSkeletonRel().SetTargets([skeleton.GetPath()])
    bindingAPI.Apply(prim)

# --------------------------------------------.
# Set BlendShape.
# --------------------------------------------.
def setBlendShape(primPath : str):
    # Get Skeleton.
    skeletonPrimPath = f"{primPath}/skeleton"
    skeletonPrim = stage.GetPrimAtPath(skeletonPrimPath)
    if not skeletonPrim.IsValid():
        return
    skeleton = UsdSkel.Skeleton(skeletonPrim)

    # Get Mesh.
    meshPrimPath = f"{primPath}/mesh"
    meshPrim = stage.GetPrimAtPath(meshPrimPath)
    if not meshPrim.IsValid():
        return
    mesh = UsdGeom.Mesh(meshPrim)

    # Create blendShape shape key.
    blendShape_key1 = UsdSkel.BlendShape.Define(stage, f"{meshPrimPath}/key1")
    blendShape_key1.CreateOffsetsAttr().Set([Gf.Vec3f(0, 0, 0), Gf.Vec3f(20, 0, 0)])
    blendShape_key1.CreatePointIndicesAttr().Set([2, 3])

    blendShape_key2 = UsdSkel.BlendShape.Define(stage, f"{meshPrimPath}/key2")
    blendShape_key2.CreateOffsetsAttr().Set([Gf.Vec3f(-20, 0, 0), Gf.Vec3f(20, 0, 0)])
    blendShape_key2.CreatePointIndicesAttr().Set([0, 1])

    # Specify an array of joint names in Mesh.
    blendShapesName = ["key1", "key2"]
    bindingAPI = UsdSkel.BindingAPI(meshPrim)
    bindingAPI.CreateBlendShapesAttr(blendShapesName)

    # Assign a BlendsShape to the Mesh.
    bindingAPI.CreateBlendShapeTargetsRel().SetTargets([blendShape_key1.GetPath(), blendShape_key2.GetPath()])

    # Create SkelAnim.
    primPath = f"{skeletonPrimPath}/skelAnim"
    skelAnim = stage.GetPrimAtPath(primPath)
    if not skelAnim.IsValid():
        skelAnim = UsdSkel.Animation.Define(stage, primPath)
    else:
        skelAnim = UsdSkel.Animation(skelAnim)
    
    # Set SkelAnim.
    UsdSkel.BindingAPI(skeletonPrim).CreateAnimationSourceRel().SetTargets([skelAnim.GetPath()])
    UsdSkel.BindingAPI.Apply(skeletonPrim)

    # Specify BlendShape for SkelAnim.
    blendShapesAttr = skelAnim.CreateBlendShapesAttr()
    blendShapesAttr.Set(blendShapesName)

    blendShapesList = [1.0, 0.0]
    attr = skelAnim.CreateBlendShapeWeightsAttr()
    attr.Set(blendShapesList)

# Create a Plane mesh with Skeleton structure.
createPlaneMeshWithSkeletonSkin("/World/plane", 100.0)

# Set BlendShape.
setBlendShape("/World/plane")


# ---------------------------------------------------------------------.
# Import PLATEAU obj for Tokyo23-ku in LOD1.
#   Specify the path where the local "13100_tokyo23-ku_2020_obj_3_op.zip" was extracted in in_plateau_obj_path.
# ---------------------------------------------------------------------.

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import glob
import os

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString

# --------------------------------------.
# Input Parameters.
# --------------------------------------.
# Source path (Root path with PLATEAU obj).
in_plateau_obj_path = "K:\\Modeling\\PLATEAU\\Tokyo_23ku\\13100_tokyo23-ku_2020_obj_3_op"

# Load LOD2.
in_load_lod2 = False

# Load map area.
mapIndexList = [533925, 533926, 533934, 533935, 533936, 533937, 533944, 533945, 533946, 533947, 533954, 533955, 533956, 533957]

# --------------------------------------.
# Path of PLATEAU data.
# --------------------------------------.

# topographic.
dem_path = in_plateau_obj_path + "/dem"

# building.
buliding_lod1_path = in_plateau_obj_path + "/bldg/lod1"
buliding_lod2_path = in_plateau_obj_path + "/bldg/lod2"

# bridge.
bridge_path = in_plateau_obj_path + "/brid"

# tran.
tran_path = in_plateau_obj_path + "/tran"

# ----------------------------------------------------.
# Convert file name to a string that can be used in USD Prim name.
# @param[in] fName   file name.
# @return  USD Prim name.
# ----------------------------------------------------.
def convFileNameToUSDPrimName (fName : str):
    # Remove extension.
    fName2 = os.path.splitext(fName)[0]

    retName = ""
    for i in range(len(fName2)):
        c = fName2[i]

        if retName == "":
            if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_':
                pass
            else:
                retName += '_'

        if (c >= '0' and c <= '9') or (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_':
            retName += c
        elif c == ' ':
            retName += '_'
        else:
            retName += str(c.encode('utf-8').hex())
 
    return retName

# --------------------------------------.
# Set rotate.
# @param[in] prim           target prim.
# @param[in] (rx, ry, rz)   Rotate (angle).
# --------------------------------------.
def setRotate (prim : Usd.Prim, rx : float, ry : float, rz : float):
    if prim.IsValid():
        tV = prim.GetAttribute("xformOp:rotateXYZ")
        if tV.IsValid():
            prim.CreateAttribute("xformOp:rotateXYZ", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(rx, ry, rz))

        tV = prim.GetAttribute("xformOp:orient")
        if tV.IsValid():
            rotX = Gf.Rotation(Gf.Vec3d(1, 0, 0), rx)
            rotY = Gf.Rotation(Gf.Vec3d(0, 1, 0), ry)
            rotZ = Gf.Rotation(Gf.Vec3d(0, 0, 1), rz)
            rotXYZ = rotZ * rotY * rotX
            q = Gf.Quatf(rotXYZ.GetQuat())
            prim.CreateAttribute("xformOp:orient", Sdf.ValueTypeNames.Quatf, False).Set(q)

# --------------------------------------.
# Create new Material (OmniPBR).
# @param[in] materialPrimPath   Prim path of Material
# @param[in] targetPrimPath     Prim path to bind Material.
# --------------------------------------.
def createMaterialOmniPBR (materialPrimPath : str, targetPrimPath : str):
    material = UsdShade.Material.Define(stage, materialPrimPath)

    shaderPath = materialPrimPath + '/Shader'
    shader = UsdShade.Shader.Define(stage, shaderPath)
    shader.SetSourceAsset('OmniPBR.mdl', 'mdl')
    shader.GetPrim().CreateAttribute('info:mdl:sourceAsset:subIdentifier', Sdf.ValueTypeNames.Token, False, Sdf.VariabilityUniform).Set('OmniPBR')

    # Set Diffuse color.
    shader.CreateInput('diffuse_color_constant', Sdf.ValueTypeNames.Color3f).Set((0.2, 0.2, 0.2))

    # Set Metallic.
    shader.CreateInput('metallic_constant', Sdf.ValueTypeNames.Float).Set(0.0)

    # Set Roughness.
    shader.CreateInput('reflection_roughness_constant', Sdf.ValueTypeNames.Float).Set(0.5)

    # Connecting Material to Shader.
    mdlOutput = material.CreateSurfaceOutput('mdl')
    mdlOutput.ConnectToSource(shader, 'out')

    # Bind material.
    if targetPrimPath != "":
        tPrim = stage.GetPrimAtPath(targetPrimPath)
        if tPrim.IsValid():
            UsdShade.MaterialBindingAPI(tPrim).Bind(material)

    return materialPrimPath

# --------------------------------------.
# Create Xform (e.g. map_533946).
# --------------------------------------.
def createXfrom_mapIndex (mapIndex : int, materialPath : str):
    mapPrimPath = defaultPrimPath + "/map_" + str(mapIndex)
    prim = stage.GetPrimAtPath(mapPrimPath)
    if prim.IsValid() == False:
        UsdGeom.Xform.Define(stage, mapPrimPath)
        prim = stage.GetPrimAtPath(mapPrimPath)

        # Bind material.
        if materialPath != "":
            matPrim = stage.GetPrimAtPath(materialPath)
            if matPrim.IsValid():
                material = UsdShade.Material(matPrim)
                UsdShade.MaterialBindingAPI(prim).Bind(material)

    return mapPrimPath

# --------------------------------------.
# load dem.
# @param[in] mapIndex       map index. 
# @param[in] materialPath   material prim path.
# --------------------------------------.
def loadDem (mapIndex : int, materialPath : str):
    if os.path.exists(dem_path) == False:
        return

    mapPrimPath = createXfrom_mapIndex(mapIndex, materialPath)
    demPrimPath = mapPrimPath + "/dem"
    UsdGeom.Xform.Define(stage, demPrimPath)

    for path in glob.glob(dem_path + "/" + str(mapIndex) + "*.obj"):

        fName = os.path.basename(path)

        # Convert Prim name.
        primName = convFileNameToUSDPrimName(fName)

        # Create Xform.
        newPath = demPrimPath + "/" + primName
        UsdGeom.Xform.Define(stage, newPath)
        prim = stage.GetPrimAtPath(newPath)

        # Remove references.
        prim.GetReferences().ClearReferences()

        # Add a reference.
        prim.GetReferences().AddReference(path)

        setRotate(prim, -90.0, 0.0, 0.0)

# --------------------------------------.
# load building.
# @param[in] mapIndex       map index. 
# @param[in] useLOD2        If LOD2 is available, use LOD2.
# @param[in] materialPath   material prim path.
# --------------------------------------.
def loadBuilding (mapIndex : int, useLOD2 : bool, materialPath : str):
    if os.path.exists(buliding_lod1_path) == False:
        return

    mapPrimPath = createXfrom_mapIndex(mapIndex, materialPath)
    buildingPath = mapPrimPath + "/building"
    UsdGeom.Xform.Define(stage, buildingPath)

    # If LOD2 exists.
    useLOD2Dict = dict()
    if useLOD2 and os.path.exists(buliding_lod2_path):
        # Search subdirectories.
        for path in glob.glob(buliding_lod2_path + "/**/" + str(mapIndex) + "*.obj", recursive=True):
            fName = os.path.basename(path)  # e.g. 53392641_bldg_6677.obj
            p1 = fName.find('_')
            if p1 > 0:
                s = fName[0:p1]
                useLOD2Dict[int(s)] = path

    # Search subdirectories.
    for path in glob.glob(buliding_lod1_path + "/**/" + str(mapIndex) + "*.obj", recursive=True):
        fName = os.path.basename(path)

        p1 = fName.find('_')
        if p1 > 0:
            s = fName[0:p1]
            mIndex = int(s)

            # Refer to LOD2 path.
            if mIndex in useLOD2Dict:
                path = useLOD2Dict[mIndex]
                fName = os.path.basename(path)

        # Conv Prim name.
        primName = convFileNameToUSDPrimName(fName)

        # Create Xform.
        newPath = buildingPath + "/" + primName
        UsdGeom.Xform.Define(stage, newPath)
        prim = stage.GetPrimAtPath(newPath)

        # Remove references.
        prim.GetReferences().ClearReferences()

        # Add a reference.
        prim.GetReferences().AddReference(path)

        setRotate(prim, -90.0, 0.0, 0.0)

# --------------------------------------.
# load PLATEAU data.
# --------------------------------------.
def load_PLATEAU ():
    if os.path.exists(in_plateau_obj_path) == False:
        return

    # Create OmniPBR material.
    materialLooksPath = "/World/Looks"
    prim = stage.GetPrimAtPath(materialLooksPath)
    if prim.IsValid() == False:
        UsdGeom.Scope.Define(stage, materialLooksPath)

    defaultMaterialPath = createMaterialOmniPBR(materialLooksPath + "/defaultMaterial", "")

    for mapIndex in mapIndexList:
        loadDem(mapIndex, defaultMaterialPath)
        loadBuilding(mapIndex, in_load_lod2, defaultMaterialPath)

# --------------------------------------.
# --------------------------------------.
load_PLATEAU()


# ---------------------------------------------------------------------.
# Import PLATEAU obj for Tokyo23-ku in LOD1.
#   Specify the path where the local "13100_tokyo23-ku_2020_obj_3_op.zip" was extracted in in_plateau_obj_path.
#
# It also assigns textures created from GeoTIFF to dem.
# Please use "divide_GeoTiff_images.py" to convert GeoTIFF into jpeg images by dividing them into 10x10 segments in advance.
# ---------------------------------------------------------------------.
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.client
import glob
import carb
import os
import asyncio
import omni.kit.asset_converter

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString
if defaultPrimPath == "":
    defaultPrimPath = "/World"

# --------------------------------------.
# Input Parameters.
# --------------------------------------.
# Source path (Root path with PLATEAU obj).
in_plateau_obj_path = "K:\\Modeling\\PLATEAU\\Tokyo_23ku\\13100_tokyo23-ku_2020_obj_3_op"

# dem textures path.
# See : divide_GeoTiff_images.py
in_dem_textures_path = "K:\\Modeling\\PLATEAU\\Tokyo_23ku\\13100_tokyo23-ku_2020_ortho_2_op\\divide_images"

# output folder.
# If specified, all usd and texture files are output to the specified folder.
in_output_folder = "omniverse://localhost/PLATEAU/Tokyo_23ku"

# Convert obj to USD (Skipped if already converted to USD).
in_convert_to_usd = True

# Folder to store output USD.
# If not specified, in_plateau_obj_path + "\\output_usd"
in_output_usd_folder = ""

# Load LOD2.
in_load_lod2 = False

# Load LOD1 & LOD2.
in_load_lod1_lod2 = False

# Assign texture to dem.
in_assign_dem_texture = True

# Load bridge.
in_load_bridge = False

# Load tran.
in_load_tran = False

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
# Pass the process to Omniverse.
# ----------------------------------------------------.
async def _omniverse_sync_wait():
    await omni.kit.app.get_app().next_update_async()

# --------------------------------------.
# Exist path (file/folder).
# Support on Nucleus.
# --------------------------------------.
async def ocl_existPath_async (path : str):
    (result, entry) = await omni.client.stat_async(path)
    if result == omni.client.Result.ERROR_NOT_FOUND:
        return False
    return True

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
            if type(tV.Get()) == Gf.Quatd:
                tV.Set(rotXYZ.GetQuat())
            elif type(tV.Get()) == Gf.Quatf:
                tV.Set(Gf.Quatf(rotXYZ.GetQuat()))

# --------------------------------------.
# Set scale.
# @param[in] prim           target prim.
# @param[in] (sx, sy, sz)   Scale.
# --------------------------------------.
def setScale (prim : Usd.Prim, sx : float, sy : float, sz : float):
    if prim.IsValid():
        tV = prim.GetAttribute("xformOp:scale")
        if tV.IsValid():
            prim.CreateAttribute("xformOp:scale", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(sx, sy, sz))

# --------------------------------------.
# Set translate.
# @param[in] prim           target prim.
# @param[in] (tx, ty, tz)   translate.
# --------------------------------------.
def setTranslate (prim : Usd.Prim, tx : float, ty : float, tz : float):
    if prim.IsValid():
        tV = prim.GetAttribute("xformOp:translate")
        if tV.IsValid():
            prim.CreateAttribute("xformOp:translate", Sdf.ValueTypeNames.Float3, False).Set(Gf.Vec3f(tx, ty, tz))

# --------------------------------------.
# Create new Material (OmniPBR).
# @param[in] materialPrimPath   Prim path of Material
# @param[in] targetPrimPath     Prim path to bind Material.
# @param[in] textureFilePath    File path of Diffuse texture.
# @param[in] diffuseColor       Diffuse Color.
# --------------------------------------.
def createMaterialOmniPBR (materialPrimPath : str, targetPrimPath : str = "", textureFilePath : str = "", diffuseColor : Gf.Vec3f = Gf.Vec3f(0.2, 0.2, 0.2)):
    material = UsdShade.Material.Define(stage, materialPrimPath)

    shaderPath = materialPrimPath + '/Shader'
    shader = UsdShade.Shader.Define(stage, shaderPath)
    shader.SetSourceAsset('OmniPBR.mdl', 'mdl')
    shader.GetPrim().CreateAttribute('info:mdl:sourceAsset:subIdentifier', Sdf.ValueTypeNames.Token, False, Sdf.VariabilityUniform).Set('OmniPBR')

    # Set Diffuse color.
    shader.CreateInput('diffuse_color_constant', Sdf.ValueTypeNames.Color3f).Set((diffuseColor[0], diffuseColor[1], diffuseColor[2]))

    # Set Metallic.
    shader.CreateInput('metallic_constant', Sdf.ValueTypeNames.Float).Set(0.0)

    # Set Roughness.
    shader.CreateInput('reflection_roughness_constant', Sdf.ValueTypeNames.Float).Set(0.8)

    # Set Specular.
    shader.CreateInput('specular_level', Sdf.ValueTypeNames.Float).Set(0.0)

    # Set texture.
    if textureFilePath != "":
        diffTexIn = shader.CreateInput('diffuse_texture', Sdf.ValueTypeNames.Asset)
        diffTexIn.Set(textureFilePath)
        diffTexIn.GetAttr().SetColorSpace('sRGB')

    # Connecting Material to Shader.
    mdlOutput = material.CreateSurfaceOutput('mdl')
    mdlOutput.ConnectToSource(shader.ConnectableAPI(), 'out')

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
# @param[in] _mapIndex       map index. 
# @param[in] _materialPath   material prim path.
# --------------------------------------.
async def loadDem (_mapIndex : int, _materialPath : str):
    if (await ocl_existPath_async(dem_path)) == False:
        return

    mapPrimPath = createXfrom_mapIndex(_mapIndex, _materialPath)
    demPrimPath = mapPrimPath + "/dem"
    UsdGeom.Xform.Define(stage, demPrimPath)

    # Scope specifying the Material.
    materialPrimPath = ""
    if in_assign_dem_texture:
        materialPrimPath = defaultPrimPath + "/Looks/map_" + str(_mapIndex)
        prim = stage.GetPrimAtPath(materialPrimPath)
        if prim.IsValid() == False:
            UsdGeom.Scope.Define(stage, materialPrimPath)

    # Must be pre-converted if using USD.
    src_dem_path = ""
    if in_convert_to_usd:
        path = in_output_usd_folder
        if path == "":
            path = in_plateau_obj_path + "/output_usd"

        if (await ocl_existPath_async(path)):
            path += "/dem/" + str(_mapIndex) + "*"
            src_dem_path = path + "/" + str(_mapIndex) + "*.usd"

    if src_dem_path == "":
        src_dem_path = dem_path + "/" + str(_mapIndex) + "*.obj"

    for path in glob.glob(src_dem_path, recursive=True):
        fName = os.path.basename(path)

        # Get map index from file name.
        mapIndex = 0
        p1 = fName.find('_')
        if p1 > 0:
            mapIndex = int(fName[0:p1])

        # When usd file is output on Nucleus, check the corresponding file.
        if in_output_folder != "":
            fName2 = str(mapIndex) + "_dem.usd"
            newPath = in_output_folder + "/data"
            newPath += "/dem/" + str(mapIndex) + "/" + fName2
            if (await ocl_existPath_async(newPath)):
                path = newPath

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
        setScale(prim, 100.0, 100.0, 100.0)

        # Assign texture.
        if in_assign_dem_texture and mapIndex > 0:
            mapFilePath = in_dem_textures_path + "/" + str(mapIndex) + ".jpg"

            if in_output_folder != "":
                mapFilePath2 = in_output_folder + "/data/geotiff_images"
                mapFilePath2 += "/" + str(mapIndex) + ".jpg"
                if (await ocl_existPath_async(mapFilePath2)):
                    mapFilePath = mapFilePath2

            if (await ocl_existPath_async(mapFilePath)):
                # Create material.
                materialName = "mat_dem_" + str(mapIndex)
                matPath = materialPrimPath + "/" + materialName
                createMaterialOmniPBR(matPath, newPath, mapFilePath)

        # Pass the process to Omniverse.
        asyncio.ensure_future(_omniverse_sync_wait())

# --------------------------------------.
# load building.
# @param[in] _mapIndex       map index. 
# @param[in] _useLOD2        If LOD2 is available, use LOD2.
# @param[in] _materialPath   material prim path.
# --------------------------------------.
async def loadBuilding (_mapIndex : int, _useLOD2 : bool, _materialPath : str):
    if (await ocl_existPath_async(buliding_lod1_path)) == False:
        return

    mapPrimPath = createXfrom_mapIndex(_mapIndex, _materialPath)
    buildingPath = mapPrimPath + "/building"
    if _useLOD2:
        buildingPath += "_lod2"
    else:
        buildingPath += "_lod1"

    UsdGeom.Xform.Define(stage, buildingPath)

    # Must be pre-converted if using USD.
    src_bldg_path = ""
    if in_convert_to_usd:
        path = in_output_usd_folder
        if path == "":
            path = in_plateau_obj_path + "/output_usd"

        if (await ocl_existPath_async(path)):
            path += "/building/lod2/" + str(_mapIndex) + "*"
            src_bldg_path = path + "/" + str(_mapIndex) + "*.usd"

    if src_bldg_path == "":
        src_bldg_path = buliding_lod2_path + "/**/" + str(_mapIndex) + "*.obj"

    # If LOD2 exists.
    useLOD2Dict = dict()
    if _useLOD2 and (await ocl_existPath_async(buliding_lod2_path)):
        # Search subdirectories.
        for path in glob.glob(src_bldg_path, recursive=True):
            fName = os.path.basename(path)  # e.g. 53392641_bldg_6677.obj
            p1 = fName.find('_')
            if p1 > 0:
                s = fName[0:p1]

                # When usd file is output on Nucleus, check the corresponding file.
                if in_output_folder != "":
                    mIndex = int(s)
                    fName2 = str(mIndex) + "_bldg.usd"
                    newPath = in_output_folder + "/data"
                    newPath += "/building/lod2/" + str(mIndex) + "/" + fName2
                    if (await ocl_existPath_async(newPath)):
                        path = newPath

                useLOD2Dict[int(s)] = path

    # Must be pre-converted if using USD.
    src_bldg_path = ""
    if in_convert_to_usd:
        path = in_output_usd_folder
        if path == "":
            path = in_plateau_obj_path + "/output_usd"

        if (await ocl_existPath_async(path)):
            path += "/building/lod1/" + str(_mapIndex) + "*"
            src_bldg_path = path + "/" + str(_mapIndex) + "*.usd"

    if src_bldg_path == "":
        src_bldg_path = buliding_lod1_path + "/**/" + str(_mapIndex) + "*.obj"

    # Search subdirectories.
    for path in glob.glob(src_bldg_path, recursive=True):
        fName = os.path.basename(path)

        chkF = False
        p1 = fName.find('_')
        if p1 > 0:
            s = fName[0:p1]
            mIndex = int(s)

            # When usd file is output on Nucleus, check the corresponding file.
            if (not in_load_lod1_lod2) or (in_load_lod1_lod2 and not _useLOD2):
                if in_output_folder != "":
                    fName2 = str(mIndex) + "_bldg.usd"
                    newPath = in_output_folder + "/data"
                    newPath += "/building/lod1/" + str(mIndex) + "/" + fName2
                    if (await ocl_existPath_async(newPath)):
                        path = newPath
                        chkF = True
                
            # Refer to LOD2 path.
            if mIndex in useLOD2Dict:
                path = useLOD2Dict[mIndex]
                fName = os.path.basename(path)
                chkF = True

        if not chkF:
            continue

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
        setScale(prim, 100.0, 100.0, 100.0)

        # Pass the process to Omniverse.
        asyncio.ensure_future(_omniverse_sync_wait())

# --------------------------------------.
# load bridge.
# @param[in] _mapIndex       map index. 
# @param[in] _materialPath   material prim path.
# --------------------------------------.
async def loadBridge (_mapIndex : int, _materialPath : str):
    if (await ocl_existPath_async(bridge_path)) == False:
        return

    mapPrimPath = createXfrom_mapIndex(_mapIndex, _materialPath)
    bridgePath = mapPrimPath + "/bridge"
    UsdGeom.Xform.Define(stage, bridgePath)

    # Must be pre-converted if using USD.
    src_brid_path = ""
    if in_convert_to_usd:
        path = in_output_usd_folder
        if path == "":
            path = in_plateau_obj_path + "/output_usd"

        if (await ocl_existPath_async(path)):
            path += "/bridge/" + str(_mapIndex) + "*"
            src_brid_path = path + "/" + str(_mapIndex) + "*.usd"

    if src_brid_path == "":
        src_brid_path = bridge_path + "/**/" + str(_mapIndex) + "*.obj"

    # Search subdirectories.
    for path in glob.glob(src_brid_path, recursive=True):
        fName = os.path.basename(path)

        mIndex = 0
        p1 = fName.find('_')
        if p1 > 0:
            s = fName[0:p1]
            mIndex = int(s)
        if mIndex == 0:
            continue

        # Conv Prim name.
        primName = convFileNameToUSDPrimName(fName)

        # When usd file is output on Nucleus, check the corresponding file.
        if in_output_folder != "":
            fName2 = str(mIndex) + "_brid.usd"
            newPath = in_output_folder + "/data"
            newPath += "/bridge/" + str(mIndex) + "/" + fName2
            if (await ocl_existPath_async(newPath)):
                path = newPath

        # Create Xform.
        newPath = bridgePath + "/" + primName
        UsdGeom.Xform.Define(stage, newPath)
        prim = stage.GetPrimAtPath(newPath)

        # Remove references.
        prim.GetReferences().ClearReferences()

        # Add a reference.
        prim.GetReferences().AddReference(path)

        setRotate(prim, -90.0, 0.0, 0.0)
        setScale(prim, 100.0, 100.0, 100.0)

        # Pass the process to Omniverse.
        asyncio.ensure_future(_omniverse_sync_wait())

# --------------------------------------.
# load tran.
# @param[in] _mapIndex       map index. 
# @param[in] _materialPath   material prim path.
# --------------------------------------.
async def loadTran (_mapIndex : int, _materialPath : str):
    if (await ocl_existPath_async(tran_path)) == False:
        return

    mapPrimPath = createXfrom_mapIndex(_mapIndex, _materialPath)
    tranPath = mapPrimPath + "/tran"
    UsdGeom.Xform.Define(stage, tranPath)

    # Must be pre-converted if using USD.
    src_tran_path = ""
    if in_convert_to_usd:
        path = in_output_usd_folder
        if path == "":
            path = in_plateau_obj_path + "/output_usd"

        if (await ocl_existPath_async(path)):
            path += "/tran/" + str(_mapIndex) + "*"
            src_tran_path = path + "/" + str(_mapIndex) + "*.usd"

    if src_tran_path == "":
        src_tran_path = tran_path + "/**/" + str(_mapIndex) + "*.obj"

    # Search subdirectories.
    for path in glob.glob(src_tran_path, recursive=True):
        fName = os.path.basename(path)

        mIndex = 0
        p1 = fName.find('_')
        if p1 > 0:
            s = fName[0:p1]
            mIndex = int(s)
        if mIndex == 0:
            continue

        # Conv Prim name.
        primName = convFileNameToUSDPrimName(fName)

        # When usd file is output on Nucleus, check the corresponding file.
        if in_output_folder != "":
            fName2 = str(mIndex) + "_tran.usd"
            newPath = in_output_folder + "/data"
            newPath += "/tran/" + str(mIndex) + "/" + fName2
            if (await ocl_existPath_async(newPath)):
                path = newPath

        # Create Xform.
        newPath = tranPath + "/" + primName
        UsdGeom.Xform.Define(stage, newPath)
        prim = stage.GetPrimAtPath(newPath)

        # Remove references.
        prim.GetReferences().ClearReferences()

        # Add a reference.
        prim.GetReferences().AddReference(path)

        setRotate(prim, -90.0, 0.0, 0.0)
        setScale(prim, 100.0, 100.0, 100.0)

        heightPos = 5.0
        setTranslate(prim, 0.0, heightPos, 0.0)

        # Create/Set material.
        matPath = "/World/Looks/mat_trans"
        primM = stage.GetPrimAtPath(matPath)
        if not primM.IsValid():
            col = Gf.Vec3f(0, 1, 0)
            createMaterialOmniPBR(matPath, "", "", col)
            primM = stage.GetPrimAtPath(matPath)
        
        material = UsdShade.Material(primM)
        UsdShade.MaterialBindingAPI(prim).Bind(material)

        # Pass the process to Omniverse.
        asyncio.ensure_future(_omniverse_sync_wait())

# --------------------------------------.
# Convert obj files to USD.
# --------------------------------------.

# Get target path for converting dem obj to usd.
async def get_ObjToUsdDem (_mapIndex : int, _dstPath : str):
    if (await ocl_existPath_async(dem_path)) == False:
        return

    dstPath = _dstPath + "/dem"
    if (await ocl_existPath_async(dstPath)) == False:
        result = omni.client.create_folder(dstPath)
        if result != omni.client.Result.OK:
            return

    srcObjPathList = []
    dstUsdPathList = []
    for path in glob.glob(dem_path + "/" + str(_mapIndex) + "*.obj"):
        fName = os.path.basename(path)

        # Get map index from file name.
        mapIndex = 0
        p1 = fName.find('_')
        if p1 > 0:
            mapIndex = int(fName[0:p1])

        dstPath2 = dstPath + "/" + str(mapIndex)
        if (await ocl_existPath_async(dstPath2)) == False:
            omni.client.create_folder(dstPath2)

        usdPath = dstPath2 + "/" + str(mapIndex) + "_dem.usd"
        if (await ocl_existPath_async(usdPath)):
            continue

        srcObjPathList.append(path)
        dstUsdPathList.append(usdPath)

    return srcObjPathList, dstUsdPathList

# Get target path for converting bldg obj to usd.
async def get_ObjToUsdBuilding (_mapIndex : int, _dstPath : str):
    srcObjPathList = []
    dstUsdPathList = []

    if (await ocl_existPath_async(buliding_lod1_path)):
        dstPath = _dstPath + "/building/lod1"

        for path in glob.glob(buliding_lod1_path + "/**/" + str(_mapIndex) + "*.obj", recursive=True):
            if (await ocl_existPath_async(dstPath)) == False:
                omni.client.create_folder(dstPath)

            fName = os.path.basename(path)

            # Get map index from file name.
            mapIndex = 0
            p1 = fName.find('_')
            if p1 > 0:
                mapIndex = int(fName[0:p1])

            dstPath2 = dstPath + "/" + str(mapIndex)
            if (await ocl_existPath_async(dstPath2)) == False:
                omni.client.create_folder(dstPath2)

            usdPath = dstPath2 + "/" + str(mapIndex) + "_bldg.usd"
            if (await ocl_existPath_async(usdPath)):
                continue

            srcObjPathList.append(path)
            dstUsdPathList.append(usdPath)

    if (await ocl_existPath_async(buliding_lod2_path)) and in_load_lod2:
        dstPath = _dstPath + "/building/lod2"

        for path in glob.glob(buliding_lod2_path + "/**/" + str(_mapIndex) + "*.obj", recursive=True):
            if (await ocl_existPath_async(dstPath)) == False:
                omni.client.create_folder(dstPath)

            fName = os.path.basename(path)

            # Get map index from file name.
            mapIndex = 0
            p1 = fName.find('_')
            if p1 > 0:
                mapIndex = int(fName[0:p1])

            dstPath2 = dstPath + "/" + str(mapIndex)
            if (await ocl_existPath_async(dstPath2)) == False:
                omni.client.create_folder(dstPath2)

            usdPath = dstPath2 + "/" + str(mapIndex) + "_bldg.usd"
            if (await ocl_existPath_async(usdPath)):
                continue

            srcObjPathList.append(path)
            dstUsdPathList.append(usdPath)

    return srcObjPathList, dstUsdPathList

# Get target path for converting bridge obj to usd.
async def get_ObjToUsdBridge (_mapIndex : int, _dstPath : str):
    srcObjPathList = []
    dstUsdPathList = []

    if (await ocl_existPath_async(bridge_path)):
        dstPath = _dstPath + "/bridge"

        for path in glob.glob(bridge_path + "/**/" + str(_mapIndex) + "*.obj", recursive=True):
            if (await ocl_existPath_async(dstPath)) == False:
                omni.client.create_folder(dstPath)

            fName = os.path.basename(path)

            # Get map index from file name.
            mapIndex = 0
            p1 = fName.find('_')
            if p1 > 0:
                mapIndex = int(fName[0:p1])

            dstPath2 = dstPath + "/" + str(mapIndex)
            if (await ocl_existPath_async(dstPath2)) == False:
                omni.client.create_folder(dstPath2)

            usdPath = dstPath2 + "/" + str(mapIndex) + "_brid.usd"
            if (await ocl_existPath_async(usdPath)):
                continue

            srcObjPathList.append(path)
            dstUsdPathList.append(usdPath)

    return srcObjPathList, dstUsdPathList

# Get target path for converting tran obj to usd.
async def get_ObjToUsdTran (_mapIndex : int, _dstPath : str):
    srcObjPathList = []
    dstUsdPathList = []

    if (await ocl_existPath_async(tran_path)):
        dstPath = _dstPath + "/tran"
        if (await ocl_existPath_async(dstPath)) == False:
            omni.client.create_folder(dstPath)

        for path in glob.glob(tran_path + "/**/" + str(_mapIndex) + "*.obj", recursive=True):
            fName = os.path.basename(path)

            # Get map index from file name.
            mapIndex = 0
            p1 = fName.find('_')
            if p1 > 0:
                mapIndex = int(fName[0:p1])

            dstPath2 = dstPath + "/" + str(mapIndex)
            if (await ocl_existPath_async(dstPath2)) == False:
                omni.client.create_folder(dstPath2)

            usdPath = dstPath2 + "/" + str(mapIndex) + "_tran.usd"
            if (await ocl_existPath_async(usdPath)):
                continue

            srcObjPathList.append(path)
            dstUsdPathList.append(usdPath)

    return srcObjPathList, dstUsdPathList

# Convert asset file(obj/fbx/glTF, etc) to usd.
async def convert_asset_to_usd (input_path_list, output_path_list):
    # Input options are defaults.
    converter_context = omni.kit.asset_converter.AssetConverterContext()
    converter_context.ignore_materials = False
    converter_context.ignore_camera = False
    converter_context.ignore_animations = False
    converter_context.ignore_light = False
    converter_context.export_preview_surface = False
    converter_context.use_meter_as_world_unit = False
    converter_context.create_world_as_default_root_prim = True
    converter_context.embed_textures = True
    converter_context.convert_fbx_to_y_up = False
    converter_context.convert_fbx_to_z_up = False
    converter_context.merge_all_meshes = False
    converter_context.use_double_precision_to_usd_transform_op = False 
    converter_context.ignore_pivots = False 
    converter_context.keep_all_materials = True
    converter_context.smooth_normals = True
    instance = omni.kit.asset_converter.get_instance()

    for i in range(len(input_path_list)):
        input_asset = input_path_list[i]
        output_usd  = output_path_list[i]
        task = instance.create_converter_task(input_asset, output_usd, None, converter_context)

        # Wait for completion.
        success = await task.wait_until_finished()
        if not success:
            carb.log_error(task.get_status(), task.get_detailed_error())
            break

# convert obj(dem/dldg/drid/tran) to usd.
async def convertObjToUsd ():
    if (await ocl_existPath_async(in_plateau_obj_path)) == False:
        return

    dstPath = in_output_usd_folder
    if dstPath == "":
        dstPath = in_plateau_obj_path + "/output_usd"

    if in_output_folder != "":
        dstPath = in_output_folder + "/data"

    if (await ocl_existPath_async(dstPath)) == False:
        result = omni.client.create_folder(dstPath)
        if result != omni.client.Result.OK:
            return

    srcObjPathList = []
    dstUsdPathList = []
    for mapIndex in mapIndexList:
        ##sList, dList = get_ObjToUsdDem(mapIndex, dstPath)
        sList, dList = await get_ObjToUsdDem(mapIndex, dstPath)

        srcObjPathList.extend(sList)
        dstUsdPathList.extend(dList)

    for mapIndex in mapIndexList:
        #sList, dList = get_ObjToUsdBuilding(mapIndex, dstPath)
        sList, dList = await get_ObjToUsdBuilding(mapIndex, dstPath)
        srcObjPathList.extend(sList)
        dstUsdPathList.extend(dList)

    if in_load_bridge:
        for mapIndex in mapIndexList:
            #sList, dList = get_ObjToUsdBridge(mapIndex, dstPath)
            sList, dList = await get_ObjToUsdBridge(mapIndex, dstPath)
            srcObjPathList.extend(sList)
            dstUsdPathList.extend(dList)

    if in_load_tran:
        for mapIndex in mapIndexList:
            #sList, dList = get_ObjToUsdTran(mapIndex, dstPath)
            sList, dList = await get_ObjToUsdTran(mapIndex, dstPath)
            srcObjPathList.extend(sList)
            dstUsdPathList.extend(dList)

    # Wait for usd conversion.
    if len(srcObjPathList) > 0:
        task = asyncio.create_task(convert_asset_to_usd(srcObjPathList, dstUsdPathList))
        await task
        print(f"PLATEAU : convert obj to usd ({ len(srcObjPathList) })")

        asyncio.ensure_future(_omniverse_sync_wait())

# Copy geoTiff images.
async def copyGEOTiffImages (srcPath : str, _mapIndex : int):
    if in_output_folder == "":
        return

    if (await ocl_existPath_async(srcPath)) == False:
        return

    dstPath = in_output_folder + "/data/geotiff_images"
    if (await ocl_existPath_async(dstPath)) == False:
        result = omni.client.create_folder(dstPath)
        if result != omni.client.Result.OK:
            return

    imgCou = 0
    for path in glob.glob(srcPath + "/" + str(_mapIndex) + "*.*"):
        fName = os.path.basename(path)

        dPath = dstPath + "/" + fName
        if (await ocl_existPath_async(dPath)):
            continue

        try:
            # TODO : Warning ?
            result = omni.client.copy(path, dPath)
            if result == omni.client.Result.OK:
                imgCou += 1
        except:
            pass
    
    if imgCou > 0:
        print(f"PLATEAU : copy GEOTiff images ({ imgCou })")
    

# --------------------------------------.
# load PLATEAU data.
# --------------------------------------.
async def load_PLATEAU ():
    if (await ocl_existPath_async(in_plateau_obj_path)) == False:
        return

    print("PLATEAU : Start processing.")

    # Convert obj to usd.
    if in_convert_to_usd:
        task = asyncio.create_task(convertObjToUsd())
        await task

    # Copy GEOTiff images.
    if in_dem_textures_path != "":
        for mapIndex in mapIndexList:
            await copyGEOTiffImages(in_dem_textures_path, mapIndex)

    # Create OmniPBR material.
    materialLooksPath = defaultPrimPath + "/Looks"
    prim = stage.GetPrimAtPath(materialLooksPath)
    if prim.IsValid() == False:
        UsdGeom.Scope.Define(stage, materialLooksPath)

    defaultMaterialPath = createMaterialOmniPBR(materialLooksPath + "/defaultMaterial")

    for mapIndex in mapIndexList:
        task_dem = asyncio.create_task(loadDem(mapIndex, defaultMaterialPath))
        await task_dem

        if not in_load_lod1_lod2:
            task_building = asyncio.create_task(loadBuilding(mapIndex, in_load_lod2, defaultMaterialPath))
            await task_building
        else:
            task_building_lod1 = asyncio.create_task(loadBuilding(mapIndex, False, defaultMaterialPath))
            await task_building_lod1

            task_building_lod2 = asyncio.create_task(loadBuilding(mapIndex, True, defaultMaterialPath))
            await task_building_lod2

        if in_load_bridge and in_load_lod2:
            task_bridge = asyncio.create_task(loadBridge(mapIndex, defaultMaterialPath))
            await task_bridge

        if in_load_tran:
            task_tran = asyncio.create_task(loadTran(mapIndex, defaultMaterialPath))
            await task_tran

        print(f"PLATEAU : map_index[{mapIndex}]")

    print("PLATEAU : Processing is complete.")

# --------------------------------------.
# --------------------------------------.
asyncio.ensure_future(load_PLATEAU())

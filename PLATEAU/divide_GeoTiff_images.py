# ---------------------------------------------------------------------.
# PLATEAU GeoTIFF images split 10x10 and saved as jpeg.
# ---------------------------------------------------------------------.
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.kit.commands
import glob
import os
from PIL import Image

# Allows handling of large size images.
Image.MAX_IMAGE_PIXELS = 1000000000

# --------------------------------------.
# Input Parameters.
# --------------------------------------.
# Source path (Root path with PLATEAU GeoTIFF).
in_plateau_obj_path = "K:\\Modeling\\PLATEAU\\Tokyo_23ku\\13100_tokyo23-ku_2020_ortho_2_op"

# Folder to save the split images.
in_save_folder_path = "K:\\Modeling\\PLATEAU\\Tokyo_23ku\\13100_tokyo23-ku_2020_ortho_2_op\\divide_images"

# --------------------------------------.
# Load image and divide (10 x 10).
# --------------------------------------.
def load_divideImage (filePath : str, savePath : str):
    fName = os.path.basename(filePath)

    # Remove extension.
    fName2 = os.path.splitext(fName)[0]

    try:
        srcImage = Image.open(filePath)

        # Get image size.
        wid = srcImage.size[0]
        hei = srcImage.size[1]

        # 10x10 division.
        wid_10 = (int)((float)(wid) / 10.0) 
        hei_10 = (int)((float)(hei) / 10.0)

        index = 0
        iy1 = hei_10 * 9
        for y in range(10):
            ix1 = 0
            for x in range(10):
                img = srcImage.crop((ix1, iy1, ix1 + wid_10, iy1 + hei_10))

                # Save file name ('533925' + '02' ==> '53392502.jpg').
                dstName = fName2 + str(index).zfill(2) + ".jpg"
                dstPath = savePath + "/" + dstName

                img.save(dstPath)

                index += 1
                ix1 += wid_10
            iy1 -= hei_10

    
    except Exception as e:
        pass

# --------------------------------------.
# Divide GeoTiff images.
# --------------------------------------.
def divide_geoTiff (savePath : str):
    if os.path.exists(in_plateau_obj_path) == False:
        return

    # Create a save folder.
    if os.path.exists(in_save_folder_path) == False:
        os.makedirs(in_save_folder_path)

    # Divide and save images.
    for path in glob.glob(in_plateau_obj_path + "/images/*.tif"):
        load_divideImage(path, savePath)

        fName = os.path.basename(path)
        print("Divide [" + fName + "]")

# --------------------------------------.
# --------------------------------------.
divide_geoTiff(in_save_folder_path)
print("Save success !!")




from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import math

def rgb_to_srgb (v : float, quantum_max : float = 1.0):
    if v <= 0.0031308:
        return (v * 12.92)
    v = v / quantum_max
    v = math.pow(v, 1.0 / 2.4) * 1.055 - 0.055
    return (v * quantum_max)

def srgb_to_rgb (v : float, quantum_max : float = 1.0):
    v = v / quantum_max
    if v <= 0.04045:
        return (v / 12.92)
    v = math.pow((v + 0.055) / 1.055, 2.4)
    return (v * quantum_max)

# Conv RGB to sRGB.
def conv_RGB_to_sRGB (col : Gf.Vec3f):
    retCol = Gf.Vec3f(col)

    if retCol[0] > 0.0 and retCol[0] < 1.0:
        retCol[0] = rgb_to_srgb(retCol[0])

    if retCol[1] > 0.0 and retCol[1] < 1.0:
        retCol[1] = rgb_to_srgb(retCol[1])

    if retCol[2] > 0.0 and retCol[2] < 1.0:
        retCol[2] = rgb_to_srgb(retCol[2])
    
    return retCol

# Conv sRGB to RGB (Linear).
def conv_sRGB_to_RGB (col : Gf.Vec3f):
    retCol = Gf.Vec3f(col)

    if retCol[0] > 0.0 and retCol[0] < 1.0:
        retCol[0] = srgb_to_rgb(retCol[0])

    if retCol[1] > 0.0 and retCol[1] < 1.0:
        retCol[1] = srgb_to_rgb(retCol[1])

    if retCol[2] > 0.0 and retCol[2] < 1.0:
        retCol[2] = srgb_to_rgb(retCol[2])

    return retCol

# ---------------------------------------.

# Original color (sRGB).
col = Gf.Vec3f(0.5, 0.4, 0.7)

# sRGB to RGB (sRGB to linear).
col_linear = conv_sRGB_to_RGB(col)

# RGB to sRGB (linear to sRGB).
col2 = conv_RGB_to_sRGB(col_linear)

print("col : " + str(col))
print("col_linear : " + str(col_linear))
print("col2 : " + str(col2))

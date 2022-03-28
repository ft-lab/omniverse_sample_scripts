from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf, Tf

try:
    # Open USD File.
    ret = omni.usd.get_context().open_stage("xxx.usd")
    print("open_stage : " + str(ret))

except Exception as e:
    print(e)

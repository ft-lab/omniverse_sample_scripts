from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

try:
    # Open USD File.
    usdPath = "https://ft-lab.github.io/usd/omniverse/usd/cyawan/cyawan.usdc"
    ret = omni.usd.get_context().open_stage(usdPath)

    if ret == True:
        # Get stage.
        stage = omni.usd.get_context().get_stage()

        # Convert relative paths to absolute paths from Stage.
        # It is necessary to specify the relative path where the texture name, Reference, etc. exists on the Stage.
        absPath = stage.ResolveIdentifierToEditTarget("./cyawan_mat_albedo.png")

        # "https://ft-lab.github.io/usd/omniverse/usd/cyawan/cyawan_mat_albedo.png"
        print(absPath)

except Exception as e:
    print(e)

from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

xformCache = UsdGeom.XformCache(0)

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print(f"[ {prim.GetName()} ]")

        # Calc local matrix.
        matrix = xformCache.GetLocalTransformation(prim)[0]
        print(matrix)

        # Decompose matrix.
        # If the result is False, then reduce the value of eps and call Factor again.
        eps = 1e-10
        result = matrix.Factor(eps)
        if result[0]:
            scale = result[2]
            rotate = result[3].ExtractRotation()
            translation = result[4]

            # Convert Rotate to Euler.
            # Rotate XYZ.
            rotateE = rotate.Decompose(Gf.Vec3d(0, 0, 1), Gf.Vec3d(0, 1, 0), Gf.Vec3d(1, 0, 0))
            rotateE = Gf.Vec3d(rotateE[2], rotateE[1], rotateE[0])

            print(f"Translation : {translation}")
            print(f"rotate : {rotateE}")
            print(f"scale : {scale}")



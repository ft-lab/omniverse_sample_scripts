from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        # Order of Transform elements.
        transformOrder = prim.GetAttribute('xformOpOrder')

        if transformOrder.IsValid() and transformOrder.Get() != None:
            print('    TransformOrder : ' + str(transformOrder.Get()))

            for transV in transformOrder.Get():
                # 'xformOp:scale', 'xformOp:rotateXYZ', 'xformOp:translate', etc.
                tV = prim.GetAttribute(transV)

                if tV.IsValid():
                    print("    " + transV + " ( " + str(tV.GetTypeName()) + " ) : " + str(tV.Get()))


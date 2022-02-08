from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == False:
        continue
    
    try:
        gprim = UsdGeom.Gprim(prim)
        doubleSidedAttr = gprim.GetDoubleSidedAttr()
        if doubleSidedAttr != None and doubleSidedAttr.IsValid():
            # Get doubleSided (True/False).
            # The Omniverse Viewport does not reflect "doubleSided", but "singleSided".
            if doubleSidedAttr.Get() != None:
                print("[" + prim.GetName() + "] doubleSided : " + str(doubleSidedAttr.Get()))
            
                # Set DoubleSided.
                #doubleSidedAttr.Set(True)

    except Exception as e:
        print(e)    

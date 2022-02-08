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
        singleSidedAttr = prim.GetAttribute("singleSided")
        if singleSidedAttr != None and singleSidedAttr.IsValid():
            # Get singleSided (True/False).
            if singleSidedAttr.Get() != None:
                print("[" + prim.GetName() + "] singleSided : " + str(singleSidedAttr.Get()))

        # Set singleSided.
        #if prim.GetTypeName() == 'Mesh':
        #    singleSidedAttr = prim.CreateAttribute("singleSided", Sdf.ValueTypeNames.Bool)
        #    singleSidedAttr.Set(True)

    except Exception as e:
        print(e)    

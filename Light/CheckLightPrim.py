from pxr import Usd, UsdGeom, UsdPhysics, UsdLux, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# Check if prim is Light.
def checkLight(prim : Usd.Prim):
    if prim.IsA(UsdLux.DistantLight) or prim.IsA(UsdLux.CylinderLight) or \
      prim.IsA(UsdLux.DiskLight) or prim.IsA(UsdLux.DomeLight) or \
      prim.IsA(UsdLux.RectLight) or prim.IsA(UsdLux.SphereLight):
    
        lightAPI = UsdLux.LightAPI(prim)
        if lightAPI:
            print(f"intensity : {lightAPI.GetIntensityAttr().Get()}")
            print(f"color : {lightAPI.GetColorAttr().Get()}")
            print(f"exposure : {lightAPI.GetExposureAttr().Get()}")

        shapingAPI = UsdLux.ShapingAPI(prim)
        if shapingAPI:
            print(f"cone angle : {shapingAPI.GetShapingConeAngleAttr().Get()}")
            print(f"cone softness : {shapingAPI.GetShapingConeSoftnessAttr().Get()}")

        return True    

    return False

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)

    if checkLight(prim):
        print(f"[ {prim.GetPath().pathString} ] : {prim.GetTypeName()}")

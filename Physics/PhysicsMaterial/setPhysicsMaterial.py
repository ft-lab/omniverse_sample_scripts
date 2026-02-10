from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

def definePhysicsMaterial(primPath: str):
    prim = stage.GetPrimAtPath(primPath)
    if not prim.IsValid():
        material = UsdShade.Material.Define(stage, primPath)
    prim = material.GetPrim()

    if prim.GetTypeName() != "Material":
        return None
    
    # Specify the parameters of the Physics Material.
    materialAPI = UsdPhysics.MaterialAPI(prim)
    materialAPI.Apply(prim)

    attr = materialAPI.CreateDynamicFrictionAttr()
    attr.Set(0.01)

    attr = materialAPI.CreateStaticFrictionAttr()
    attr.Set(0.02)

    attr = materialAPI.CreateRestitutionAttr()
    attr.Set(0.03)

    attr = materialAPI.CreateDensityAttr()
    attr.Set(10)

    return prim

def bindPhysicsMaterial(primPath: str, materialPath: str):
    prim = stage.GetPrimAtPath(primPath)
    if not prim.IsValid():
        return None
    
    materialPrim = stage.GetPrimAtPath(materialPath)
    if not materialPrim.IsValid() or materialPrim.GetTypeName() != "Material":
        return None
    
    materialBindingAPI = UsdShade.MaterialBindingAPI(prim)

    materialBindingAPI.UnbindDirectBinding("physics")
    rel = materialBindingAPI.GetDirectBindingRel("physics")
    if materialPath == "":
        return
    
    rel.AddTarget(materialPath)
    materialBindingAPI.SetMaterialBindingStrength(rel, "weakerThanDescendants")
    materialBindingAPI.Apply(prim)

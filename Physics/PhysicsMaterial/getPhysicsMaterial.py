from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

path="/World/PhysicsMaterials/PhysicsMaterial_02"
prim = stage.GetPrimAtPath(path)
if prim.IsValid():
  if prim.GetTypeName() == "Material":
    materialAPI = UsdPhysics.MaterialAPI(prim)
    
    attr = materialAPI.GetDynamicFrictionAttr()
    if attr and attr.IsDefined():
        print(f"Dynamic Friction: {attr.Get()}")

    attr = materialAPI.GetStaticFrictionAttr()
    if attr and attr.IsDefined():
        print(f"Static Friction: {attr.Get()}")

    attr = materialAPI.GetRestitutionAttr()
    if attr and attr.IsDefined():
        print(f"Restruction: {attr.Get()}")

    attr = materialAPI.GetDensityAttr()
    if attr and attr.IsDefined():
        print(f"Density: {attr.Get()}")



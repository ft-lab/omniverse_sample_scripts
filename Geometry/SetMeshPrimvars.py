from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim.GetTypeName() != "Mesh": 
        continue

    m = UsdGeom.Mesh(prim)

    # USD 22.11 : The specification has been changed to use UsdGeom.PrimvarsAPI.

    # Set primvar(float).
    primvarV = UsdGeom.PrimvarsAPI(prim).CreatePrimvar("dat1", Sdf.ValueTypeNames.Float)
    attr = primvarV.GetAttr()
    attr.Set((2.2))

    if UsdGeom.primvarV(prim).HasPrimvar("dat1"):    # Check primvar.
        # Remove primvar.
        UsdGeom.primvarV(prim).RemovePrimvar("dat1")

    # Set primvar (float2).
    # If there is already a primvar with the same name but a different type,
    # it must be removed using RemoveProperty.
    primvarV = UsdGeom.PrimvarsAPI(prim).CreatePrimvar("dat1", Sdf.ValueTypeNames.Float2)
    attr = primvarV.GetAttr()
    attr.Set((1.0, 2.0))

    # Set primvar (color).
    primvarV = UsdGeom.PrimvarsAPI(prim).CreatePrimvar("dat2", Sdf.ValueTypeNames.Color3f)
    attr = primvarV.GetAttr()
    attr.Set((1.0, 0.5, 0.2))

    # Set primvar (float3 array)
    primvarV = UsdGeom.PrimvarsAPI(prim).CreatePrimvar("dat3", Sdf.ValueTypeNames.Float3Array)
    attr = primvarV.GetAttr()
    attr.Set([(0.1, 0.2, 0.5), (0.4, 0.05, 0.0), (0.1, 0.4, 0.05)])


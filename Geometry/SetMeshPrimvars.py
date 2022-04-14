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

    # Set primvar(float).
    primvar = m.CreatePrimvar("dat1", Sdf.ValueTypeNames.Float)
    primvar.Set(2.2)

    if m.HasPrimvar("dat1"):    # Check primvar.
        # Remove primvar.
        prim.RemoveProperty("primvars:dat1")

    # Set primvar (float2).
    # If there is already a primvar with the same name but a different type,
    # it must be removed using RemoveProperty.
    primvar = m.CreatePrimvar("dat1", Sdf.ValueTypeNames.Float2)
    primvar.Set((1.0, 2.0))

    # Set primvar (color).
    primvar = m.CreatePrimvar("dat2", Sdf.ValueTypeNames.Color3f)
    primvar.Set((1.0, 0.5, 0.2))

    # Set primvar (float3 array)
    primvar = m.CreatePrimvar("dat3", Sdf.ValueTypeNames.Float3Array)
    primvar.Set([(0.1, 0.2, 0.5), (0.4, 0.05, 0.0), (0.1, 0.4, 0.05)])


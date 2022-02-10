from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, UsdSkel, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# ------------------------------------------------------------.
# Flip mesh normals.
# ------------------------------------------------------------.
def FlipMeshNormals (prim):
    if prim.GetTypeName() == 'Mesh':
        m = UsdGeom.Mesh(prim)

        # If it is displayed.
        if m.ComputeVisibility() == 'inherited':
            # Get prim path.
            path = prim.GetPath().pathString



            print(prim.GetName())

    pChildren = prim.GetChildren()
    for cPrim in pChildren:
        FlipMeshNormals(cPrim)

# ------------------------------------------------------------.

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid():
        FlipMeshNormals(prim)



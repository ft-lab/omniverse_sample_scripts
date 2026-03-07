import random

from pxr import Gf, Usd, UsdGeom
import omni.usd

def create_vertex_display_color(prim: Usd.Prim):
    """
    Create vertex display color for the specified prim.
    This assigns a random color to each vertex of the mesh.
    """
    geomPrim = UsdGeom.Gprim(prim)
    if not geomPrim:
        print(f"Prim at path {prim.GetPath()} is not a Gprim.")
        return
    
    if not prim.IsA(UsdGeom.Mesh):
        print(f"Prim at path {prim.GetPath()} is not a Mesh.")
        return

    # Specify "vertex" to assign DisplayColor to each vertex.
    geomPrim.CreateDisplayColorPrimvar(UsdGeom.Tokens.vertex)

    # Number of mesh vertices.
    pointsAttr = UsdGeom.Mesh(prim).GetPointsAttr().Get()
    vertices_count = len(pointsAttr)

    # Assign random colors to the mesh vertices.
    colors = []
    for i in range(vertices_count):
        color_r = random.random()
        color_g = random.random()
        color_b = random.random()
        col = Gf.Vec3f(color_r, color_g, color_b)
        colors.append(col)
    geomPrim.CreateDisplayColorAttr(colors)


# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim:
        create_vertex_display_color(prim)


import random

from pxr import Gf, Usd, UsdGeom
import omni.usd

def create_uniform_display_color(prim: Usd.Prim):
    """
    Create uniform display color for the specified prim.
    This assigns a random color to each face of the mesh.
    """
    geomPrim = UsdGeom.Gprim(prim)
    if not geomPrim:
        print(f"Prim at path {prim.GetPath()} is not a Gprim.")
        return
    
    if not prim.IsA(UsdGeom.Mesh):
        print(f"Prim at path {prim.GetPath()} is not a Mesh.")
        return

    # Specify "uniform" to assign DisplayColor to each face.
    geomPrim.CreateDisplayColorPrimvar(UsdGeom.Tokens.uniform)

    # Number of mesh faces.
    face_vertex_counts = UsdGeom.Mesh(prim).GetFaceVertexCountsAttr().Get()
    faces_count = len(face_vertex_counts)
    print(f"faces_count: {faces_count}")

    # Assign random colors to the mesh faces.
    colors = []
    for i in range(faces_count):
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
        create_uniform_display_color(prim)


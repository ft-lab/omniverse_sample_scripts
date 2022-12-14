from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get prim.
path = "/World/Sphere"
prim = stage.GetPrimAtPath(path)

if prim.IsValid():
    # Rename prim.

    # Prepare specified paths as candidates for rename.
    # "/World/Sphere" to "/World/Sphere2"
    edit = Sdf.NamespaceEdit.Rename(path, "Sphere2")
    batchE = Sdf.BatchNamespaceEdit()
    batchE.Add(edit)

    # Execute rename.
    stage.GetEditTarget().GetLayer().Apply(batchE)
    

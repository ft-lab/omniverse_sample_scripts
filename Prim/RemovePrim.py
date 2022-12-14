from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get prim.
path = "/World/Sphere"
prim = stage.GetPrimAtPath(path)

if prim.IsValid():
    # Remove prim.
    # See here : https://graphics.pixar.com/usd/release/api/class_usd_stage.html#ac605faad8fc2673263775b1eecad2955
    # For example, if Prim is used in a layer, RemovePrim will not remove it completely.
    #stage.RemovePrim(path)

    # Prepare specified paths as candidates for deletion.
    edit = Sdf.NamespaceEdit.Remove(path)
    batchE = Sdf.BatchNamespaceEdit()
    batchE.Add(edit)

    # Execute Deletion.
    stage.GetEditTarget().GetLayer().Apply(batchE)
    

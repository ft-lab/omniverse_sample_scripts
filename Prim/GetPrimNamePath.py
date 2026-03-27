import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get prim.
orgPath = "/World/defaultLight"
prim = stage.GetPrimAtPath(orgPath)

if prim.IsValid():
    # Get Prim name.
    name = prim.GetName()
    print(f"Name : {name}")

    # Get Prim path.
    path = prim.GetPath()
    print(f"Path : {path}")

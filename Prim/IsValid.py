import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

path = "/World"

# Get prim.
prim = stage.GetPrimAtPath(path)

# Use IsValid to check if the specified Prim exists.
print(f"{path} : {prim.IsValid()}")

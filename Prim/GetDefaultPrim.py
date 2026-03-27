import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()

# Default prim path.
defaultPrimPath = defaultPrim.GetPath().pathString

print(f"DefaultPrim : {defaultPrimPath}")
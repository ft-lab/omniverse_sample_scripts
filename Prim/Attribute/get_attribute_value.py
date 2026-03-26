import omni.usd

# Specify the attribute name to retrieve
ATTR_NAME = "user:myFloat"

stage = omni.usd.get_context().get_stage()
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()
if not paths:
    paths = ["/World"]

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        print(f"Invalid prim: {path}")
        continue

    attr = prim.GetAttribute(ATTR_NAME)
    if not attr:
        print(f"Attribute {ATTR_NAME} not found on {path}")
        continue

    val = attr.Get()
    print(f"{path} :: {ATTR_NAME} = {val}")

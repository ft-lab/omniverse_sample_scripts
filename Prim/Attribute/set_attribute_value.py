import omni.usd

# Settings: attribute name to change and the new value
ATTR_NAME = "user:myFloat"
NEW_VALUE = 2.5

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
        # If the attribute does not exist, create it before setting
        attr = prim.CreateAttribute(ATTR_NAME, None, False)

    attr.Set(NEW_VALUE)
    print(f"Set {ATTR_NAME} on {path} = {NEW_VALUE}")

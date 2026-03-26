import omni.usd

# Attribute name to remove
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

    try:
        # RemoveProperty expects the property name as string
        propName = attr.GetName()
        prim.RemoveProperty(propName)
        print(f"Removed attribute {ATTR_NAME} from {path}")
    except Exception as e:
        print(f"Failed to remove {ATTR_NAME} on {path}: {e}")

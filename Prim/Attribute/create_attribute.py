from pxr import Sdf
import omni.usd

# Settings: specify attribute name, type and default value here
ATTR_NAME = "user:myFloat"
ATTR_TYPE = Sdf.ValueTypeNames.Float
DEFAULT_VALUE = 1.0

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

    # Create attribute and set default value
    attr = prim.CreateAttribute(ATTR_NAME, ATTR_TYPE, False)
    attr.Set(DEFAULT_VALUE)
    print(f"Created attribute {ATTR_NAME} on {path} = {DEFAULT_VALUE}")

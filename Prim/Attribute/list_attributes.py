import omni.usd

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

    attrs = prim.GetAttributes()
    if not attrs:
        print(f"No attributes on {path}")
        continue

    print(f"Attributes on {path}:")
    for a in attrs:
        try:
            t = a.GetTypeName()
        except Exception:
            t = None

        # Try to get the attribute value; protect against exceptions and long outputs
        try:
            v = a.Get()
            v_str = str(v)
            if len(v_str) > 200:
                v_str = v_str[:200] + "..."
        except Exception:
            v_str = "<unreadable>"

        print(f" - {a.GetName()}  type={t}  value={v_str}")

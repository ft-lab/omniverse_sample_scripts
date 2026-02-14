import omni.kit.app

# e.g. 109.0.2
kit_version = omni.kit.app.get_app().get_kit_version()
kit_version = kit_version.split("+")[0] if "+" in kit_version else kit_version
print(f"Kit Version = {kit_version}")

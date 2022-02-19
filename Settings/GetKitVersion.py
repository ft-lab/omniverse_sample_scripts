import omni.kit

# Get Omniverse Kit version.
kitVersion = omni.kit.app.get_app_interface().get_build_version()

# 102.1.2+release.xxxx
print("Kit Version : " + str(kitVersion))

# 102.1.2
print(str("   ") + kitVersion.split("+")[0])


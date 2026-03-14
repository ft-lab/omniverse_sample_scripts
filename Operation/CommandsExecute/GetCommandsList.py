import omni.kit

# Get commands list (dict).
listA = omni.kit.commands.get_commands()
keys = listA.keys()

for key in keys:
    print(str(key))

# From "Bundled Extensions/omni.kit.commands" in Omniverse Kit documentation.
import omni.kit.commands
import omni.kit.undo

# Class for UNDO processing.
class MyOrange (omni.kit.commands.Command):
    def __init__ (self, bar: list):
        self._bar = bar

    def do (self):
        self._bar.append('orange')

    def undo (self):
        del self._bar[-1]

# Register a Class and run it.
omni.kit.commands.register(MyOrange)
my_list = []
omni.kit.commands.execute("MyOrange", bar=my_list)
print(my_list)

# UNDO.
omni.kit.undo.undo()
print(my_list)

# REDO.
omni.kit.undo.redo()
print(my_list)



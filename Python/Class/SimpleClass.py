# -----------------------------------------------.
# Simple class.
# -----------------------------------------------.
class ClassFoo:
    _name = ""

    # Constructor
    def __init__(self, name : str):
        self.name = name
        print("Constructor")

    # Destructor
    def __del__(self):
        print("Destructor")

    def printName (self):
        print("name = " + self.name)

    def add (self, a : float, b : float):
        return (a + b)

# -----------------------------------------------.

# Create new class.
foo = ClassFoo("test")

foo.printName()
print(foo.add(12.5, 8.2))

# Destroying a class.
foo = None

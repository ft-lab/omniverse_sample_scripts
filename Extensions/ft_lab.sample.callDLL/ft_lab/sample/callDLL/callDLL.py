import omni.ext

from ctypes import *

# Load library.
# Add the search path for [[native.library]] to "config/extension.toml".
dll = cdll.LoadLibrary(r"OmniverseSimpleDLL.dll")

# ----------------------------------------------------.
# Call external function.
# ----------------------------------------------------.
def callExtFunc():
    if dll == None:
        return

    v = dll.ext_add(3, 8)
    print("dll.ext_add(3, 8) : " + str(v))

    v2 = dll.ext_sub(3, 8)
    print("dll.ext_sub(3, 8) : " + str(v2))

# ----------------------------------------------------.
class CallDLLExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        print("[ft_lab.sample.callDLL] HelloExtension startup")
        callExtFunc()

    def on_shutdown(self):
        print("[ft_lab.sample.callDLL] HelloExtension shutdown")


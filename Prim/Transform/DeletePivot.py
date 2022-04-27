from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf
import omni.usd
import omni.kit.commands

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

# --------------------------------------------------.
# Delete pivot.
# --------------------------------------------------.
def _deletePivot (prim : Usd.Prim):
    if prim == None:
        return

    path = prim.GetPath().pathString + ".xformOp:translate:pivot"
    omni.kit.commands.execute('RemoveProperty', prop_path=path)

    transformOrder = prim.GetAttribute("xformOpOrder").Get()
    if transformOrder != None:
        orderList = []
        for sV in transformOrder:
            if sV == "xformOp:translate:pivot" or sV == "!invert!xformOp:translate:pivot":
                continue
            orderList.append(sV)

        prim.GetAttribute("xformOpOrder").Set(orderList)

# --------------------------------------------------.
for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid() == True:
        # Print prim name.
        print('[ ' + prim.GetName() + ' ]')

        # Delete pivot.
        _deletePivot(prim)


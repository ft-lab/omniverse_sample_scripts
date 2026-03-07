from pxr import Usd
import omni.usd

def get_variant_info(prim: Usd.Prim):
    """
    Get variant information of the specified prim.
    """
    # Get variant sets name.
    variantSets = prim.GetVariantSets()
    print(f"variantSets: {variantSets.GetNames()}")

    for variantSetName in variantSets.GetNames():
        print(f"[{variantSetName}]")

        # Get variant names.
        variant_set = prim.GetVariantSet(variantSetName)
        variant_names = variant_set.GetVariantNames()
        print(f"  variantNames: {variant_names}")

        # Get current variant selection.
        print(f"     selection: {variant_set.GetVariantSelection()}")


# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    # Get prim.
    prim = stage.GetPrimAtPath(path)
    if prim:
        get_variant_info(prim)

from pxr import Usd
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

prim_path = "/World/Chair"
prim = stage.GetPrimAtPath(prim_path)

# "variantGroup" is the name of the VariantSet to be deleted.
variant_set_name = "variantGroup"

variant_sets = prim.GetVariantSets()
if variant_sets.HasVariantSet(variant_set_name):
    # Clear variant selection.
    variant_set = prim.GetVariantSet(variant_set_name)
    variant_set.ClearVariantSelection()

    # Deletes the specified variantSet, which must be passed via SdfPrimSpec.
    stage = prim.GetStage()
    prim_path = prim.GetPath()
    for layer in stage.GetLayerStack():
        prim_spec = layer.GetPrimAtPath(prim_path)  # SdfPrimSpec
        if prim_spec and variant_set_name in prim_spec.variantSets:
            del prim_spec.variantSets[variant_set_name]
            prim_spec.variantSetNameList.Remove(variant_set_name)

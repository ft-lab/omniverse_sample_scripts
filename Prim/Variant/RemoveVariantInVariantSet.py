from pxr import Usd
import omni.usd

# Get stage.
stage = omni.usd.get_context().get_stage()

prim_path = "/World/Chair"
prim = stage.GetPrimAtPath(prim_path)

# "variantGroup" is the name of the VariantSet to be deleted.
# "chair2" is the name of the Variant to be deleted in the "variantGroup" VariantSet.
variant_set_name = "variantGroup"
variant_name = "chair2"

variant_sets = prim.GetVariantSets()
if variant_sets.HasVariantSet(variant_set_name):
    # Clear variant selection.
    variant_set = prim.GetVariantSet(variant_set_name)
    variant_set.ClearVariantSelection()

    # Retrieve the specified prim for each layer and delete the variant in the specified VariantSet.
    prim_path = prim.GetPath()
    for layer in stage.GetLayerStack():
        prim_spec = layer.GetPrimAtPath(prim_path)  # SdfPrimSpec
        if prim_spec and variant_set_name in prim_spec.variantSets:
            vset_spec = prim_spec.variantSets[variant_set_name]
            for v in vset_spec.variantList:
                if v.name == variant_name:
                    vset_spec.RemoveVariant(v)
                    break


from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Reference : https://github.com/PixarAnimationStudios/USD/blob/release/extras/usd/tutorials/authoringVariants/authorVariants.py

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get default prim.
defaultPrim = stage.GetDefaultPrim()
defaultPrimPath = defaultPrim.GetPath().pathString

# Create empty node(Xform).
path = defaultPrimPath + '/Chair'
UsdGeom.Xform.Define(stage, path)
prim = stage.GetPrimAtPath(path)

# Set VariantSet.
variantSet = prim.GetVariantSet('variantGroup')
variantSet.AddVariant('chair1')
variantSet.AddVariant('chair2')
variantSet.AddVariant('chair3')

# -----------------------------------------------.
# Set Chair.
# -----------------------------------------------.
def SetChair (index : int, path : str, colorV):
    # Create reference.
    # The USD file to be referenced should be changed to suit your environment.
    usdPath = "https://ft-lab.github.io/usd/omniverse/usd/simple_chair.usda"
    path2 = path + '/simple_chair_' + str(index)
    UsdGeom.Xform.Define(stage, path2)
    prim2 = stage.GetPrimAtPath(path2)
    prim2.GetReferences().AddReference(usdPath)

    path3 = path2 + '/simple_chair'
    targetPrim = UsdGeom.Gprim.Get(stage, path3)
    try:
        # Clear Material.
        UsdShade.MaterialBindingAPI(targetPrim).UnbindAllBindings()

        # Set Display Color.
        colorAttr = targetPrim.GetDisplayColorAttr()
        colorAttr.Set([colorV])
    except Exception as e:
        pass

# -----------------------------------------------.
# Set 'chair1'.
variantSet.SetVariantSelection("chair1")
with variantSet.GetVariantEditContext():
    SetChair(1, path, (1,0,0))

# Set 'chair2'.
variantSet.SetVariantSelection("chair2")
with variantSet.GetVariantEditContext():
    SetChair(2, path, (0,1,0))

# Set 'chair3'.
variantSet.SetVariantSelection("chair3")
with variantSet.GetVariantEditContext():
    SetChair(3, path, (0,0,1))

# Select current variant.
variantSet.SetVariantSelection("chair1")

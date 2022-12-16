# "Pcp" added below.
from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf, Pcp

# Get stage.
stage = omni.usd.get_context().get_stage()

# Get selection.
selection = omni.usd.get_context().get_selection()
paths = selection.get_selected_prim_paths()

for path in paths:
    prim = stage.GetPrimAtPath(path)
    if prim.IsValid():
        # If Prim has Reference or Payload.
        if prim.HasAuthoredReferences() or prim.HasPayload():
            query = Usd.PrimCompositionQuery.GetDirectRootLayerArcs(prim)
            qList = query.GetCompositionArcs()

            if qList != None:
                for arc in qList:
                    arcType = arc.GetArcType()
                    if arcType != Pcp.ArcTypeReference and arcType != Pcp.ArcTypePayload:
                        continue

                    # Get AssetPath.
                    editorProxy, reference = arc.GetIntroducingListEditor()
                    assetPath = reference.assetPath

                    if arcType == Pcp.ArcTypeReference:
                        print("[" + prim.GetName() + "] has reference > " + assetPath)
                    if arcType == Pcp.ArcTypePayload:
                        print("[" + prim.GetName() + "] has payload. > " + assetPath)





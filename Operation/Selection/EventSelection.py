from pxr import Usd, UsdGeom, UsdPhysics, UsdShade, Sdf, Gf, Tf

# Get context.
context = omni.usd.get_context()

# Get stage.
stage = context.get_stage()

# ---------------------------------------------.
# Selected event.
# ---------------------------------------------.
def onStageEvent(evt):
    if evt.type == int(omni.usd.StageEventType.SELECTION_CHANGED):
        # Get selection paths.
        selection = omni.usd.get_context().get_selection()
        paths = selection.get_selected_prim_paths()
        
        for path in paths:
            prim = stage.GetPrimAtPath(path)
            if prim.IsValid() == True:
                print('Selected [ ' + prim.GetName() + ' ]')

# ------------------------------------------------.
# Register for stage events.
# Specify "subs=None" to end the event.
subs = context.get_stage_event_stream().create_subscription_to_pop(onStageEvent, name="sampleStageEvent")

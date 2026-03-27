import omni.usd

stage = omni.usd.get_context().get_stage()
rootLayer = stage.GetRootLayer()
print("Root layer identifier:", rootLayer.identifier)
try:
    path = rootLayer.realPath
    print("Root layer realPath (if saved):", path)
except Exception:
    print("Root layer has no realPath (unsaved or session layer)")

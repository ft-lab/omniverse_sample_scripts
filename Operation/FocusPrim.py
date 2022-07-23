import omni.kit.viewport_legacy

try:
    viewport = omni.kit.viewport_legacy.get_viewport_interface()
    if viewport != None:
        viewport.get_viewport_window().focus_on_selected()
except:
    pass

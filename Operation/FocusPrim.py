import omni.kit.viewport

try:
    viewport = omni.kit.viewport.get_viewport_interface()
    if viewport != None:
        viewport.get_viewport_window().focus_on_selected()
except:
    pass

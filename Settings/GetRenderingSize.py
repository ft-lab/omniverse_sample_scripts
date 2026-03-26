from omni.kit.viewport.utility import get_active_viewport

# Get rendering size.
activeViewport = get_active_viewport()
width = activeViewport.resolution[0]
height = activeViewport.resolution[1]
print(f"Rendering size : {width} x {height}")


import omni.ui
import asyncio
import omni.kit.app

# Get main window viewport.
window = omni.ui.Window('Viewport')

# ------------------------------------------.
async def my_task():
    countV = 0

    print('Start task.')

    f = None
    for i in range(10):
        with window.frame:
            with omni.ui.VStack():
                with omni.ui.Placer(offset_x=20, offset_y=50):
                    # Set label.
                    f = omni.ui.Label("counter = " + str(countV), alignment=omni.ui.Alignment.LEFT_TOP)
                    f.visible = True
                    f.set_style({"color": 0xff00ffff, "font_size": 32})
        countV += 1
        await asyncio.sleep(1)    # Sleep 1sec.

    print('End task.')

    if f != None:
        f.visible = False
        f = None
# ------------------------------------------.
# Start task.
asyncio.ensure_future(my_task())


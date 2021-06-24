import omni.ui
import omni.kit.app
import carb.events
import asyncio
import time

# Get main window viewport.
window = omni.ui.Window('Viewport')

countV = 0
timeV = time.time()

# ------------------------------------------.
# Update event.
# ------------------------------------------.
def on_update(e: carb.events.IEvent):
    global countV
    global timeV

    # Process every second.
    curTimeV = time.time()
    if curTimeV - timeV > 1:
        timeV = curTimeV

        with window.frame:
            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=20, offset_y=50):
                    # Set label.
                    f = omni.ui.Label("counter = " + str(countV))
                    f.visible = True
                    f.set_style({"color": 0xff00ffff, "font_size": 32})
        countV += 1

# ------------------------------------------.
# Register for update events.
# To clear the event, specify "subs=None".
subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(on_update, name="Test update")




import omni.ui
import omni.kit.app
import carb.events

import time
import asyncio

class UpdateInterval:
    _viewportWindow = None
    _subs = None
    _visible = True
    _time = None
    _vTime = None

    def __init__(self):
        pass

    # Update event.
    def on_update (self, e: carb.events.IEvent):
        if self._viewportWindow == None:
            return

        curTime = time.time()
        diffTime = curTime - self._time
        self._time = curTime

        if self._vTime == None:
            self._vTime = curTime
        if curTime < self._vTime + 0.5 and self._visible:
            return
        self._vTime = curTime

        # Update UI.
        with self._viewportWindow.frame:
            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=20, offset_y=30):
                    # Set label.
                    fpsV = 1.0 / diffTime
                    msgStr = "Update interval(sec) : {:.5f} sec, {:.2f} fps".format(diffTime, fpsV)
                    f = omni.ui.Label(msgStr)
                    f.visible = self._visible
                    f.set_style({"color": 0xff00ffff, "font_size": 32})

    def startup (self):
        # Get main window viewport.
        self._viewportWindow = omni.ui.Window('Viewport')

        self._time = time.time()
        self._visible = True

        # Register for update event.
        self._subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(self.on_update)

    def shutdown (self):
        # Release the update event.
        async def _exitUpdateEvent ():
            self._visible = False
            await omni.kit.app.get_app().next_update_async()
            self._subs = None
            self._vTime = None
        asyncio.ensure_future(_exitUpdateEvent())
       
# -----------------------------------------.
updateI = UpdateInterval()
updateI.startup()

# Finish the process below.
#updateI.shutdown()

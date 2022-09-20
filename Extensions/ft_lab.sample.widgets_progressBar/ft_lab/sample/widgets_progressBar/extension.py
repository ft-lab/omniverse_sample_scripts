import omni.ext
import omni.ui
from pathlib import Path
import os.path
import carb.tokens
import carb.events
import time

# ----------------------------------------------------------.
class WidgetsExtension(omni.ext.IExt):
    _window = None

    _btn = None              # omni.ui.Button.
    _progressBar = None      # omni.ui.ProgressBar.
    _progressValue = 0.2     # PrograssBar value.
    _progressStart = True    # True if Progress is to proceed.

    _subs = None             # Update Events.
    _timeV = 0

    # ------------------------------------.
    # Update event.
    # ------------------------------------.
    def on_update (self, e: carb.events.IEvent):
        # Processing every 0.2 seconds.
        curTimeV = time.time()
        if curTimeV - self._timeV > 0.2:
            self._timeV = curTimeV

            # Update progressBar.
            if self._progressStart:
                self._progressValue += 0.05
                if self._progressValue > 1.0:
                    self._progressValue -= 1.0
                self._progressBar.model.set_value(self._progressValue)

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self):
        self._progressStart = True
        self._timeV = time.time()

        # Create new window.
        self._window = omni.ui.Window("Widgets Window(ProgressBar)", width=300, height=100)

        # Callback when button is clicked.
        def onButtonClicked (self):
            if self._progressStart:
                self._progressStart = False
            else:
                self._progressStart = True

            # Change button text.
            if self._progressStart:
                self._btn.text = "Stop"
            else:
                self._btn.text = "Start"

        # ------------------------------------------.
        with self._window.frame:
            # Create window UI.
            with omni.ui.VStack(height=0):
                # ------------------------------------------.
                # ProgressBar & Button.
                # ------------------------------------------.
                omni.ui.Spacer(height=4)
                self._progressBar = omni.ui.ProgressBar(height=14, style={"color": 0xffdd0000})
                self._progressBar.model.set_value(self._progressValue)
                omni.ui.Spacer(height=4)

                self._btn = omni.ui.Button(" Button ") 
                self._btn.set_clicked_fn(lambda s = self : onButtonClicked(s))

                if self._progressStart:
                    self._btn.text = "Stop"
                else:
                    self._btn.text = "Start"

                omni.ui.Spacer(height=4)

        # Register for update events.
        # To clear the event, specify "subs=None".
        self._subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(self.on_update)

    # ------------------------------------------------.
    # Term window.
    # ------------------------------------------------.
    def term_window (self):
        if self._subs != None:
            self._subs = None

        if self._window != None:
            self._window = None

    # ------------------------------------------------.
    # Startup.
    # ------------------------------------------------.
    def on_startup(self, ext_id):
        self.init_window()

    # ------------------------------------------------.
    # Shutdown.
    # ------------------------------------------------.
    def on_shutdown(self):
        self.term_window()

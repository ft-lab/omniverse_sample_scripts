from pxr import Usd, UsdGeom, UsdSkel, UsdShade, Sdf, Gf, Tf

import carb
import carb.input
import carb.events
import omni.kit.app
import omni.ext

# ------------------------------------------.
# Input with Keyboard.
# ------------------------------------------.
class InputKeyboard:
    _keyboard = None
    _input    = None
    _keyboard_subs = None
    _update_subs   = None
    _window = None
    _keyboard_input_value = None

    def __init__(self):
        pass

    # Keyboard event.
    def _keyboard_event (self, event):
        if event.type == carb.input.KeyboardEventType.KEY_PRESS:
            self._keyboard_input_value = event.input
            print("KEY_PRESS : " + str(event.input))
        if event.type == carb.input.KeyboardEventType.KEY_RELEASE:
            print("KEY_RELEASE : " + str(event.input))
        return True

    # UI Update event.
    def _on_update (self, e: carb.events.IEvent):
        with self._window.frame:
            with omni.ui.VStack(height=0):
                with omni.ui.Placer(offset_x=20, offset_y=50):
                    # Set label.
                    f = omni.ui.Label("Input : " + str(self._keyboard_input_value))
                    f.visible = True
                    f.set_style({"color": 0xff00ffff, "font_size": 20})

    def startup (self):
        # Assign keyboard event.
        appwindow = omni.appwindow.get_default_app_window()
        self._keyboard = appwindow.get_keyboard()
        self._input    = carb.input.acquire_input_interface()
        self._keyboard_subs = self._input.subscribe_to_keyboard_events(self._keyboard, self._keyboard_event)

        # Get main window viewport.
        self._window = omni.ui.Window('Viewport')

        # Assing update event.
        self._update_subs = omni.kit.app.get_app().get_update_event_stream().create_subscription_to_pop(self._on_update, name="update")

    def shutdown (self):
        # Release update event.
        self._update_subs.unsubscribe()

        # Release keyboard event.
        self._input.unsubscribe_to_keyboard_events(self._keyboard, self._keyboard_subs)

        self._keyboard_subs = None
        self._keyboard      = None
        self._input = None
        self._update_subs = None

# -----------------------------------------.
keyboardV = InputKeyboard()
keyboardV.startup()

# stop.
#keyboardV.shutdown()


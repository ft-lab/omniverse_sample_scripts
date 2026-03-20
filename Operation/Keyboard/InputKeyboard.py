from pxr import Usd, UsdGeom, UsdSkel, UsdShade, Sdf, Gf, Tf

import carb
import carb.input
import omni.kit.app

# Reference:
# https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/carb.input.html

# ------------------------------------------.
# Input with Keyboard.
# ------------------------------------------.
class InputKeyboard:
    _keyboard = None
    _input    = None
    _keyboard_subs = None

    def __init__(self):
        pass

    # Keyboard event.
    def _keyboard_event(self, event : carb.input.KeyboardEvent):
        if event.type == carb.input.KeyboardEventType.KEY_PRESS:
            print(f"KEY_PRESS : {event.input}")
        if event.type == carb.input.KeyboardEventType.KEY_RELEASE:
            print(f"KEY_RELEASE : {event.input}")
        return True

    def startup(self):
        # Assign keyboard event.
        appwindow = omni.appwindow.get_default_app_window()
        self._keyboard = appwindow.get_keyboard()
        self._input    = carb.input.acquire_input_interface()
        try:
            self._keyboard_subs = self._input.subscribe_to_keyboard_events(self._keyboard, self._keyboard_event)
        except Exception:
            self._keyboard_subs = None

    def shutdown(self):
        # Release keyboard event.
        if self._input is not None and self._keyboard_subs is not None:
            try:
                self._input.unsubscribe_to_keyboard_events(self._keyboard, self._keyboard_subs)
            except Exception:
                pass

        self._keyboard_subs = None
        self._keyboard      = None
        self._input = None

# -----------------------------------------.
keyboardV = InputKeyboard()
keyboardV.startup()

# stop.
#keyboardV.shutdown()


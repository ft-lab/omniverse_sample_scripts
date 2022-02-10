from pxr import Usd, UsdGeom, UsdSkel, UsdPhysics, UsdShade, Sdf, Gf, Tf

import carb
import carb.input
import omni.kit.app
import omni.ext

# Reference : kit/exts/omni.kit.debug.input

# ------------------------------------------.
# Gamepad discription.
# ------------------------------------------.
class GamepadDesc:
    def _cleanup(self):
        self.name = None
        self.guid = None
        self.gamepad_device = None
        self.input_device = None
        self.is_connected = False

        self.input_val = {}

    def __init__(self):
        self._cleanup()

    def __del__(self):
        self._cleanup()

# ------------------------------------------.
# Input with GamePad.
# ------------------------------------------.
class InputGamePad:
    _gamepads = None
    _input = None
    _input_provider = None
    _gamepad_connection_subs = None
    _gamepad_inputs = None

    _app = None
    _pre_update_sub = None

    def __init__(self):
        pass

    def _update_gamepad_connection_state(self, gamepad_device, connection_state):
        for gamepad_desc in self._gamepads:
            if gamepad_desc.gamepad_device == gamepad_device:
                gamepad_desc.is_connected = connection_state

    # gamepad connection event.
    def _gamepad_connection_event(self, event):
        # Gamepad created.
        if event.type == carb.input.GamepadConnectionEventType.CREATED:
            gamepad_desc = GamepadDesc()
            gamepad_desc.name = self._input.get_gamepad_name(event.gamepad)
            gamepad_desc.guid = self._input.get_gamepad_guid(event.gamepad)
            gamepad_desc.gamepad_device = event.gamepad
            gamepad_desc.input_device = event.device
            self._gamepads.append(gamepad_desc)
            print("carb.input.GamepadConnectionEventType.CREATED")
            print("name : " + str(gamepad_desc.name))
            print("guid : " + str(gamepad_desc.guid))

        # Gamepad destroyed.
        elif event.type == carb.input.GamepadConnectionEventType.DESTROYED:
            for gamepad_desc in self._gamepads:
                if gamepad_desc.gamepad_device == event.gamepad:
                    self._gamepads.remove(gamepad_desc)
            print("carb.input.GamepadConnectionEventType.DESTROYED")

        # Gamepad connected.
        elif event.type == carb.input.GamepadConnectionEventType.CONNECTED:
            self._update_gamepad_connection_state(event.gamepad, True)
            print(" carb.input.GamepadConnectionEventType.CONNECTED")

        # Gamepad disconnected.
        elif event.type == carb.input.GamepadConnectionEventType.DISCONNECTED:
            self._update_gamepad_connection_state(event.gamepad, False)
            print(" carb.input.GamepadConnectionEventType.DISCONNECTED")

    # gamepad update event.
    def _update_gamepads_data(self, event):
        for gamepad_desc in self._gamepads:
            for gamepad_input in self._gamepad_inputs:
                # Store value.
                val = self._input.get_gamepad_value(gamepad_desc.gamepad_device, gamepad_input)
                gamepad_desc.input_val[gamepad_input] = float(val)

                # gamepad_input : DPAD (0.0 or 1.0).
                #   carb.input.GamepadInput.DPAD_DOWN
                #   carb.input.GamepadInput.DPAD_UP
                #   carb.input.GamepadInput.DPAD_LEFT
                #   carb.input.GamepadInput.DPAD_RIGHT

                # gamepad_input : buttons (0.0 or 1.0).
                #   carb.input.GamepadInput.X
                #   carb.input.GamepadInput.Y
                #   carb.input.GamepadInput.A
                #   carb.input.GamepadInput.B
                #   carb.input.GamepadInput.MENU1 (Back)
                #   carb.input.GamepadInput.MENU2 (Start)

                # gamepad_input : stick (0.0 - 1.0).
                #   carb.input.GamepadInput.LEFT_STICK_DOWN
                #   carb.input.GamepadInput.LEFT_STICK_UP
                #   carb.input.GamepadInput.LEFT_STICK_LEFT
                #   carb.input.GamepadInput.LEFT_STICK_RIGHT
                #   carb.input.GamepadInput.RIGHT_STICK_DOWN
                #   carb.input.GamepadInput.RIGHT_STICK_UP
                #   carb.input.GamepadInput.RIGHT_STICK_LEFT
                #   carb.input.GamepadInput.RIGHT_STICK_RIGHT

                # gamepad_input : stick push (0.0 or 1.0).
                #   carb.input.GamepadInput.LEFT_STICK 
                #   carb.input.GamepadInput.RIGHT_STICK 

                # gamepad_input : trigger (0.0 - 1.0).
                #   carb.input.GamepadInput.LEFT_TRIGGER
                #   carb.input.GamepadInput.RIGHT_TRIGGER

                # gamepad_input : shoulder (0.0 or 1.0).
                #   carb.input.GamepadInput.LEFT_SHOULDER 
                #   carb.input.GamepadInput.RIGHT_SHOULDER 

        if gamepad_desc.input_val[carb.input.GamepadInput.A] != 0.0:
            print("A")
        if gamepad_desc.input_val[carb.input.GamepadInput.B] != 0.0:
            print("B")
        if gamepad_desc.input_val[carb.input.GamepadInput.X] != 0.0:
            print("X")
        if gamepad_desc.input_val[carb.input.GamepadInput.Y] != 0.0:
            print("Y")
        if gamepad_desc.input_val[carb.input.GamepadInput.MENU1] != 0.0:
            print("Back")
        if gamepad_desc.input_val[carb.input.GamepadInput.MENU2] != 0.0:
            print("Start")

        if gamepad_desc.input_val[carb.input.GamepadInput.LEFT_SHOULDER] != 0.0:
            print("Left shoulder")
        if gamepad_desc.input_val[carb.input.GamepadInput.RIGHT_SHOULDER] != 0.0:
            print("Right shoulder")

        if gamepad_desc.input_val[carb.input.GamepadInput.LEFT_STICK] != 0.0:
            print("Push Left stick")
        if gamepad_desc.input_val[carb.input.GamepadInput.RIGHT_STICK] != 0.0:
            print("Push Right stick")

        v = gamepad_desc.input_val[carb.input.GamepadInput.LEFT_TRIGGER]
        if v != 0.0:
            print("Left trigger : " + str(v))

        v = gamepad_desc.input_val[carb.input.GamepadInput.RIGHT_TRIGGER]
        if v != 0.0:
            print("Right trigger : " + str(v))

    def startup (self):
        self._gamepads = []
        self._input = carb.input.acquire_input_interface()
        self._input_provider = carb.input.acquire_input_provider()
        self._gamepad_connection_subs = self._input.subscribe_to_gamepad_connection_events(self._gamepad_connection_event)

        # Creating a dict of processed GamepadInput enumeration for convenience
        def filter_gamepad_input_attribs(attr):
            return not callable(getattr(carb.input.GamepadInput, attr)) and not attr.startswith("__") and attr != "name" and attr != "COUNT"
        self._gamepad_inputs = dict((getattr(carb.input.GamepadInput, attr), attr) for attr in dir(carb.input.GamepadInput) if filter_gamepad_input_attribs(attr))

        self._app = omni.kit.app.get_app()
        self._pre_update_sub = self._app.get_pre_update_event_stream().create_subscription_to_pop(
            self._update_gamepads_data, name="GamePad test"
        )

    def shutdown (self):
        self._input.unsubscribe_to_gamepad_connection_events(self._gamepad_connection_subs)

        self._gamepad_connection_subs = None
        self._gamepad_inputs = None
        self._gamepads = None

        self._app = None
        self._pre_update_sub = None
        self._input_provider = None
        self._input = None

gamePadV = InputGamePad()
gamePadV.startup()

# stop.
#gamePadV.shutdown()


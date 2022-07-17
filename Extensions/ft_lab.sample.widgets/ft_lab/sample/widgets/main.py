import omni.ext
import omni.ui
from pathlib import Path

# ----------------------------------------------------------.
class WidgetsExtension(omni.ext.IExt):
    _window = None
 
    _sField = None
    _label0 = None

    _radioCollection = None
    _label1 = None

    _checkbox = None
    _label2 = None

    _combobox = None
    _label3 = None

    _slider = None
    _label4 = None

    # ------------------------------------------------.
    # Init window.
    # ------------------------------------------------.
    def init_window (self):
        imagesPath = Path(__file__).parent.joinpath("images")

        # Create new window.
        self._window = omni.ui.Window("Widgets Window", width=300, height=400)

        # Radio Button Style.
        style = {
            "": {"background_color": 0x0, "image_url": f"{imagesPath}/radio_off.svg"},
            ":checked": {"image_url": f"{imagesPath}/radio_on.svg"},
        }

        def onButtonClicked (uiFieldModel, uiLabel):
            if not uiFieldModel or not uiLabel:
                return

            v = uiFieldModel.model.get_value_as_string()
            uiLabel.text = "Input : " + v

        def onRadioValueChanged (uiFieldModel, uiLabel):
            if not uiFieldModel or not uiLabel:
                return

            v = uiFieldModel.get_value_as_int()
            uiLabel.text = "Select Radio : " + str(v)

        def onCheckBoxValueChanged (uiFieldModel, uiLabel):
            if not uiFieldModel or not uiLabel:
                return

            b = uiFieldModel.get_value_as_bool()
            uiLabel.text = "CheckBox : " + str(b)

        def onComboBoxValueChanged (uiFieldModel, uiLabel):
            if not uiFieldModel or not uiLabel:
                return

            v = uiFieldModel.get_value_as_int()
            uiLabel.text = "ComboBox : " + str(v)

        def onSliderValueChanged (uiFieldModel, uiLabel):
            if not uiFieldModel or not uiLabel:
                return

            v = uiFieldModel.get_value_as_float()
            uiLabel.text = "Slider : " + str(v)

        # ------------------------------------------.
        with self._window.frame:
            # Create window UI.
            with omni.ui.VStack(height=0):
                # ------------------------------------------.
                # StringField & Button.
                # ------------------------------------------.
                omni.ui.Spacer(height=4)
                self._sField = omni.ui.StringField(width=120, height=14, style={"color": 0xffffffff})
                self._sField.model.set_value("xxx")
                omni.ui.Spacer(height=4)

                omni.ui.Spacer(height=4)
                btn = omni.ui.Button(" Button ") 
                omni.ui.Spacer(height=4)

                # Label.
                with omni.ui.HStack(width=0):
                    omni.ui.Spacer(width=8)
                    self._label0 = omni.ui.Label("")

                btn.set_clicked_fn(lambda s = self._sField, l = self._label0: onButtonClicked(s, l))

                # Separator.
                omni.ui.Spacer(height=4)
                omni.ui.Line(style={"border_width":2, "color":0xff202020})
                omni.ui.Spacer(height=4)

                # ------------------------------------------.
                # Radio Button.
                # ------------------------------------------.
                # Radio button.
                self._radioCollection = omni.ui.RadioCollection()
                radioLBtnList = []
                with omni.ui.HStack(width=0):
                    for i in range(3):
                        with omni.ui.HStack(style=style):
                            radio = omni.ui.RadioButton(radio_collection=self._radioCollection, width=30, height=30)
                            omni.ui.Label(f"Radio {i} ", name="text")
                            radioLBtnList.append(radio)

                # Label.
                with omni.ui.HStack(width=0):
                    omni.ui.Spacer(width=8)
                    self._label1 = omni.ui.Label("")

                    # Update label.
                    onRadioValueChanged(self._radioCollection.model, self._label1)

                for radio in radioLBtnList:
                    radio.set_clicked_fn(lambda f = self._radioCollection.model, l = self._label1: onRadioValueChanged(f, l))

                # Separator.
                omni.ui.Spacer(height=4)
                omni.ui.Line(style={"border_width":2, "color":0xff202020})
                omni.ui.Spacer(height=4)

                # ------------------------------------------.
                # CheckBox.
                # ------------------------------------------.
                # CheckBox
                omni.ui.Spacer(height=4)
                with omni.ui.HStack(width=0):
                    self._checkbox = omni.ui.CheckBox()
                    omni.ui.Label(" CheckBox")
                omni.ui.Spacer(height=4)
                
                # Label.
                with omni.ui.HStack(width=0):
                    omni.ui.Spacer(width=8)
                    self._label2 = omni.ui.Label("")

                    # Update label.
                    onCheckBoxValueChanged(self._checkbox.model, self._label2)

                self._checkbox.model.add_value_changed_fn(lambda f = self._checkbox.model, l = self._label2: onCheckBoxValueChanged(f, l))

                # Separator.
                omni.ui.Spacer(height=4)
                omni.ui.Line(style={"border_width":2, "color":0xff202020})
                omni.ui.Spacer(height=4)

                # ------------------------------------------.
                # ComboBox.
                # ------------------------------------------.
                # ComboBox
                omni.ui.Spacer(height=4)
                self._combobox = omni.ui.ComboBox(1, "Item1", "Item2", "Item3")
                omni.ui.Spacer(height=4)

                # Label.
                with omni.ui.HStack(width=0):
                    omni.ui.Spacer(width=8)
                    self._label3 = omni.ui.Label("")

                    # Update label.
                    onComboBoxValueChanged(self._combobox.model.get_item_value_model(), self._label3)

                cModel = self._combobox.model.get_item_value_model()
                cModel.add_value_changed_fn(lambda f = cModel, l = self._label3: onComboBoxValueChanged(f, l))

                # Separator.
                omni.ui.Spacer(height=4)
                omni.ui.Line(style={"border_width":2, "color":0xff202020})
                omni.ui.Spacer(height=4)

                # ------------------------------------------.
                # Slider.
                # ------------------------------------------.
                # Slider.
                omni.ui.Spacer(height=4)
                self._slider = omni.ui.FloatSlider(min=0.0, max=10.0)
                self._slider.model.set_value(1.2)
                omni.ui.Spacer(height=4)

                # Label.
                with omni.ui.HStack(width=0):
                    omni.ui.Spacer(width=8)
                    self._label4 = omni.ui.Label("")
                    onSliderValueChanged(self._slider.model, self._label4)

                self._slider.model.add_value_changed_fn(lambda f = self._slider.model, l = self._label4: onSliderValueChanged(f, l))

                # Separator.
                omni.ui.Spacer(height=4)
                omni.ui.Line(style={"border_width":2, "color":0xff202020})
                omni.ui.Spacer(height=4)

    # ------------------------------------------------.
    # Term window.
    # ------------------------------------------------.
    def term_window (self):
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

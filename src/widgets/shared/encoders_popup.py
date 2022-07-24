from typing import Optional
from PyQt6 import QtCore, QtWidgets, QtGui

from views._compiled.shared.encoders_popup import Ui_EncodersPopup
from views._compiled.shared.encoder_formfield import Ui_EncoderFormfield
from lib.input_parsing.parse import get_available_encoders
from lib.input_parsing.encoder import Encoder

class EncoderFormField(QtWidgets.QDialog):
    clicked = QtCore.pyqtSignal(str)
    encoder: Encoder

    def __init__(self, encoder, parent=None):
        super(EncoderFormField, self).__init__(parent)

        self.ui = Ui_EncoderFormfield()
        self.ui.setupUi(self)
        self.ui.label.setText(encoder.name)
        self.encoder = encoder

        self.ui.radioButton.clicked.connect(lambda: self.clicked.emit(self.encoder.key))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.clicked.emit(self.encoder.key)
        return super().mousePressEvent(event)

    def set_text(self, value: str):
        encoded_value = self.encoder.encode(value)
        self.ui.encodedText.setPlainText(encoded_value)

class EncodersPopup(QtWidgets.QDialog):
    encode_pressed = QtCore.pyqtSignal(Encoder, str)

    encoder_widgets: dict[str, EncoderFormField]
    selected_encoder: Optional[Encoder]

    def __init__(self, parent=None):
        super(EncodersPopup, self).__init__(parent)

        self.ui = Ui_EncodersPopup()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.saveButton.setEnabled(False)

        self.encoder_widgets = {}
        for encoder in get_available_encoders():
            formfield = EncoderFormField(encoder)

            self.encoder_widgets[encoder.key] = formfield
            self.ui.encodersLayout.addWidget(formfield)

            formfield.clicked.connect(self.select_encoding)

        self.ui.inputText.textChanged.connect(self.input_text_changed)
        self.selected_encoder = None

    def select_encoding(self, selected_key: str):
        self.ui.saveButton.setEnabled(True)
        for key, widget in self.encoder_widgets.items():
            if key == selected_key:
                self.selected_encoder = widget.encoder
                widget.ui.radioButton.setChecked(True)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 1 solid #FC6A0C; }")
            else:
                widget.ui.radioButton.setChecked(False)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

    def save(self):
        if self.selected_encoder is None:
            self.close()
            return

        self.encode_pressed.emit(self.selected_encoder, self.get_input())
        self.close()

    # def showEvent(self, event):
    #     self.load_encoders()

    def input_text_changed(self):
        for _, widget in self.encoder_widgets.items():
            widget.set_text(self.get_input())

    def set_input(self, input: str):
        self.ui.inputText.setPlainText(input)

    def get_input(self) -> str:
        return self.ui.inputText.toPlainText()

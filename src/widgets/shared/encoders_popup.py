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

    def set_text_to_encode(self, value: str):
        encoded_value = self.encoder.encode(value)
        self.ui.encodedText.setPlainText(encoded_value)

    def set_text_to_decode(self, value: str):
        try:
            decoded_value = self.encoder.decode(value)
        except Exception as ex:
            decoded_value = "Error: " + str(ex)

        self.ui.encodedText.setPlainText(decoded_value)

class EncodersPopup(QtWidgets.QDialog):
    encode = QtCore.pyqtSignal(Encoder, str)
    decode = QtCore.pyqtSignal(Encoder, str)

    encoder_widgets: dict[str, EncoderFormField]
    decoder_widgets: dict[str, EncoderFormField]

    selected_encoder: Optional[Encoder]
    selected_decoder: Optional[Encoder]

    def __init__(self, parent=None):
        super(EncodersPopup, self).__init__(parent)

        self.ui = Ui_EncodersPopup()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.saveButton.setEnabled(False)

        self.encoder_widgets = {}
        self.decoder_widgets = {}
        for encoder in get_available_encoders():
            # Setup encoder form input
            formfield = EncoderFormField(encoder)
            formfield.clicked.connect(self.select_encoding)
            self.encoder_widgets[encoder.key] = formfield
            self.ui.encodersLayout.addWidget(formfield)

            # Setup decoder form input
            formfield_decode = EncoderFormField(encoder)
            formfield_decode.clicked.connect(self.select_decoding)
            self.decoder_widgets[encoder.key] = formfield_decode
            self.ui.decodersLayout.addWidget(formfield_decode)

        self.ui.tabWidget.currentChanged.connect(self.refresh_apply_button_enabled)
        self.ui.inputText.textChanged.connect(self.input_text_changed)
        self.selected_encoder = None
        self.selected_decoder = None

    def select_encoding(self, selected_key: str):
        self.clear_selected_decoding()

        for key, widget in self.encoder_widgets.items():
            if key == selected_key:
                self.selected_encoder = widget.encoder
                widget.ui.radioButton.setChecked(True)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 1 solid #FC6A0C; }")
            else:
                widget.ui.radioButton.setChecked(False)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

        self.refresh_apply_button_enabled()

    def select_decoding(self, selected_key: str):
        self.clear_selected_encoding()

        for key, widget in self.decoder_widgets.items():
            if key == selected_key:
                self.selected_decoder = widget.encoder
                widget.ui.radioButton.setChecked(True)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 1 solid #FC6A0C; }")
            else:
                widget.ui.radioButton.setChecked(False)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

        self.refresh_apply_button_enabled()

    def clear_selected_encoding(self):
        self.selected_encoder = None

        for _, widget in self.encoder_widgets.items():
            widget.ui.radioButton.setChecked(False)
            widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

    def clear_selected_decoding(self):
        self.selected_decoder = None

        for _, widget in self.decoder_widgets.items():
            widget.ui.radioButton.setChecked(False)
            widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

    def save(self):
        if self.encode_tab_selected():
            self.encode.emit(self.selected_encoder, self.get_input())
        elif self.decode_tab_selected():
            self.decode.emit(self.selected_decoder, self.get_input())

        self.clear_selected_encoding()
        self.clear_selected_decoding()

        self.close()

    def encode_tab_selected(self) -> bool:
        return self.ui.tabWidget.currentIndex() == 0

    def decode_tab_selected(self) -> bool:
        return self.ui.tabWidget.currentIndex() == 1

    def hash_tab_selected(self) -> bool:
        return self.ui.tabWidget.currentIndex() == 0

    def refresh_apply_button_enabled(self):
        if self.encode_tab_selected():
            self.ui.saveButton.setEnabled(self.selected_encoder is not None)

        if self.decode_tab_selected():
            self.ui.saveButton.setEnabled(self.selected_decoder is not None)

    # def showEvent(self, event):
    #     self.load_encoders()

    def input_text_changed(self):
        for _, widget in self.encoder_widgets.items():
            widget.set_text_to_encode(self.get_input())

        for _, widget in self.decoder_widgets.items():
            widget.set_text_to_decode(self.get_input())

    def set_input(self, input: str):
        self.ui.inputText.setPlainText(input)

    def get_input(self) -> str:
        return self.ui.inputText.toPlainText()

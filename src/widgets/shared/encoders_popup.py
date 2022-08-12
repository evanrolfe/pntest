from typing import Optional
from PyQt6 import QtCore, QtWidgets, QtGui
from lib.input_parsing.text_tree import TreeNode

from views._compiled.shared.encoders_popup import Ui_EncodersPopup
from views._compiled.shared.encoder_formfield import Ui_EncoderFormfield
from lib.input_parsing.parse import get_available_encoders, get_available_hashers
from lib.input_parsing.encoder import Encoder
from lib.input_parsing.text_wrapper import parse_text

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

    def clear(self):
        self.ui.encodedText.setPlainText("")

class EncodersPopup(QtWidgets.QDialog):
    encode = QtCore.pyqtSignal(Encoder, str)
    decode = QtCore.pyqtSignal(Encoder, str)

    encoder_widgets: dict[str, EncoderFormField]
    decoder_widgets: dict[str, EncoderFormField]
    hasher_widgets: dict[str, EncoderFormField]

    selected_encoder: Optional[Encoder]
    selected_decoder: Optional[Encoder]
    selected_hasher: Optional[Encoder]

    tree_node: Optional[TreeNode]

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
        self.hasher_widgets = {}

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

        for hasher in get_available_hashers():
            # Setup encoder form input
            formfield = EncoderFormField(hasher)
            formfield.clicked.connect(self.select_hasher)
            self.hasher_widgets[hasher.key] = formfield
            self.ui.hashersLayout.addWidget(formfield)

        self.ui.tabWidget.currentChanged.connect(self.refresh_apply_button_enabled)
        self.ui.inputText.textChanged.connect(self.input_text_changed)

        self.selected_encoder = None
        self.selected_decoder = None
        self.selected_hasher = None

    def select_encoding(self, selected_key: str):
        self.clear_selected_decoding()
        self.clear_selected_hasher()

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
        self.clear_selected_hasher()

        for key, widget in self.decoder_widgets.items():
            if key == selected_key:
                self.selected_decoder = widget.encoder
                widget.ui.radioButton.setChecked(True)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 1 solid #FC6A0C; }")
            else:
                widget.ui.radioButton.setChecked(False)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

        self.refresh_apply_button_enabled()

    def select_hasher(self, selected_key: str):
        self.clear_selected_encoding()
        self.clear_selected_decoding()

        for key, widget in self.hasher_widgets.items():
            if key == selected_key:
                self.selected_hasher = widget.encoder
                widget.ui.radioButton.setChecked(True)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 1 solid #FC6A0C; }")
            else:
                widget.ui.radioButton.setChecked(False)
                widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

        self.refresh_apply_button_enabled()

    def clear_all(self):
        self.clear_selected_decoding()
        self.clear_selected_encoding()
        self.clear_selected_hasher()
        self.set_input("")

        for _, widget in self.encoder_widgets.items():
            widget.clear()

        for _, widget in self.decoder_widgets.items():
            widget.clear()

        for _, widget in self.hasher_widgets.items():
            widget.clear()

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

    def clear_selected_hasher(self):
        self.selected_hasher = None

        for _, widget in self.hasher_widgets.items():
            widget.ui.radioButton.setChecked(False)
            widget.setStyleSheet("QWidget#EncoderFormfield { border: 0; }")

    def save(self):
        if self.encode_tab_selected():
            self.encode.emit(self.selected_encoder, self.get_input())
        elif self.decode_tab_selected():
            self.decode.emit(self.selected_decoder, self.get_input())
        elif self.hash_tab_selected():
            self.encode.emit(self.selected_hasher, self.get_input())

        self.clear_selected_encoding()
        self.clear_selected_decoding()

        self.close()

    def encode_tab_selected(self) -> bool:
        return self.ui.tabWidget.currentIndex() == 0

    def decode_tab_selected(self) -> bool:
        return self.ui.tabWidget.currentIndex() == 1

    def hash_tab_selected(self) -> bool:
        return self.ui.tabWidget.currentIndex() == 2

    def refresh_apply_button_enabled(self):
        if self.encode_tab_selected():
            self.ui.saveButton.setEnabled(self.selected_encoder is not None)

        elif self.decode_tab_selected():
            self.ui.saveButton.setEnabled(self.selected_decoder is not None)

        elif self.hash_tab_selected():
            self.ui.saveButton.setEnabled(self.selected_hasher is not None)

    def set_decoders_visible(self, visible: bool):
        self.ui.tabWidget.setTabVisible(1, visible)

    # def showEvent(self, event):
    #     self.load_encoders()

    def input_text_changed(self):
        input = self.get_input()
        if len(input) == 0:
            return

        parsed_input = parse_text(input)
        for _, widget in self.encoder_widgets.items():
            widget.set_text_to_encode(parsed_input)

        for _, widget in self.decoder_widgets.items():
            widget.set_text_to_decode(parsed_input)

        for _, widget in self.hasher_widgets.items():
            widget.set_text_to_encode(parsed_input)

    def set_input(self, input: str):
        self.ui.inputText.setPlainText(input)

    def get_input(self) -> str:
        return self.ui.inputText.toPlainText()

    def set_transformer(self, transformer: Encoder):
        if transformer.type == Encoder.TYPE_ENCODER:
            self.ui.tabWidget.setCurrentIndex(0)
            self.select_encoding(transformer.key)

        if transformer.type == Encoder.TYPE_HASHER:
            print("-------------------> SELECTING HASHER")
            self.ui.tabWidget.setCurrentIndex(2)
            self.select_hasher(transformer.key)

    def set_tree_node(self, tree_node: TreeNode):
        self.tree_node = tree_node


# Form implementation generated from reading ui file 'src/views/shared/encoder_formfield.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_EncoderFormfield(object):
    def setupUi(self, EncoderFormfield):
        EncoderFormfield.setObjectName("EncoderFormfield")
        EncoderFormfield.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(EncoderFormfield)
        self.verticalLayout_2.setContentsMargins(2, 2, 10, 2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(EncoderFormfield)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.encodedText = QtWidgets.QPlainTextEdit(EncoderFormfield)
        self.encodedText.setMaximumSize(QtCore.QSize(16777215, 40))
        self.encodedText.setObjectName("encodedText")
        self.horizontalLayout_2.addWidget(self.encodedText)
        self.radioButton = QtWidgets.QRadioButton(EncoderFormfield)
        self.radioButton.setText("")
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(EncoderFormfield)
        QtCore.QMetaObject.connectSlotsByName(EncoderFormfield)

    def retranslateUi(self, EncoderFormfield):
        _translate = QtCore.QCoreApplication.translate
        EncoderFormfield.setWindowTitle(_translate("EncoderFormfield", "Form"))
        self.label.setText(_translate("EncoderFormfield", "Base64 Encode:"))

# Form implementation generated from reading ui file 'src/views/shared/request_body_form.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RequestBodyForm(object):
    def setupUi(self, RequestBodyForm):
        RequestBodyForm.setObjectName("RequestBodyForm")
        RequestBodyForm.resize(880, 521)
        self.verticalLayout = QtWidgets.QVBoxLayout(RequestBodyForm)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.requestBodyInput = QtWidgets.QPlainTextEdit(RequestBodyForm)
        self.requestBodyInput.setObjectName("requestBodyInput")
        self.verticalLayout.addWidget(self.requestBodyInput)

        self.retranslateUi(RequestBodyForm)
        QtCore.QMetaObject.connectSlotsByName(RequestBodyForm)

    def retranslateUi(self, RequestBodyForm):
        pass

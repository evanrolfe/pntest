# Form implementation generated from reading ui file 'src/views/clients/client_view.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ClientView(object):
    def setupUi(self, ClientView):
        ClientView.setObjectName("ClientView")
        ClientView.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ClientView)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clientBodyText = QtWidgets.QPlainTextEdit(ClientView)
        self.clientBodyText.setObjectName("clientBodyText")
        self.horizontalLayout.addWidget(self.clientBodyText)

        self.retranslateUi(ClientView)
        QtCore.QMetaObject.connectSlotsByName(ClientView)

    def retranslateUi(self, ClientView):
        _translate = QtCore.QCoreApplication.translate
        ClientView.setWindowTitle(_translate("ClientView", "Form"))

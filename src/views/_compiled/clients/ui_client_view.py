# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'client_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ClientView(object):
    def setupUi(self, ClientView):
        if not ClientView.objectName():
            ClientView.setObjectName(u"ClientView")
        ClientView.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(ClientView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.clientBodyText = QPlainTextEdit(ClientView)
        self.clientBodyText.setObjectName(u"clientBodyText")

        self.horizontalLayout.addWidget(self.clientBodyText)


        self.retranslateUi(ClientView)

        QMetaObject.connectSlotsByName(ClientView)
    # setupUi

    def retranslateUi(self, ClientView):
        ClientView.setWindowTitle(QCoreApplication.translate("ClientView", u"Form", None))
    # retranslateUi


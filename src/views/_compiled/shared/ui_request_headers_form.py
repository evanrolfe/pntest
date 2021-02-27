# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_headers_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_RequestHeadersForm(object):
    def setupUi(self, RequestHeadersForm):
        if not RequestHeadersForm.objectName():
            RequestHeadersForm.setObjectName(u"RequestHeadersForm")
        RequestHeadersForm.resize(880, 521)
        self.verticalLayout = QVBoxLayout(RequestHeadersForm)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.headersTable = QTableView(RequestHeadersForm)
        self.headersTable.setObjectName(u"headersTable")

        self.verticalLayout.addWidget(self.headersTable)


        self.retranslateUi(RequestHeadersForm)

        QMetaObject.connectSlotsByName(RequestHeadersForm)
    # setupUi

    def retranslateUi(self, RequestHeadersForm):
        pass
    # retranslateUi


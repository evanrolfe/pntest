# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'headers_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_HeadersForm(object):
    def setupUi(self, HeadersForm):
        if not HeadersForm.objectName():
            HeadersForm.setObjectName(u"HeadersForm")
        HeadersForm.resize(880, 521)
        self.verticalLayout = QVBoxLayout(HeadersForm)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.headerLine = QLineEdit(HeadersForm)
        self.headerLine.setObjectName(u"headerLine")

        self.verticalLayout.addWidget(self.headerLine)

        self.headersTable = QTableView(HeadersForm)
        self.headersTable.setObjectName(u"headersTable")

        self.verticalLayout.addWidget(self.headersTable)


        self.retranslateUi(HeadersForm)

        QMetaObject.connectSlotsByName(HeadersForm)
    # setupUi

    def retranslateUi(self, HeadersForm):
        pass
    # retranslateUi


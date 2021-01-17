# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clients_table.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ClientsTable(object):
    def setupUi(self, ClientsTable):
        if not ClientsTable.objectName():
            ClientsTable.setObjectName(u"ClientsTable")
        ClientsTable.resize(424, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClientsTable.sizePolicy().hasHeightForWidth())
        ClientsTable.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(ClientsTable)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.clientsTable = QTableView(ClientsTable)
        self.clientsTable.setObjectName(u"clientsTable")

        self.horizontalLayout.addWidget(self.clientsTable)


        self.retranslateUi(ClientsTable)

        QMetaObject.connectSlotsByName(ClientsTable)
    # setupUi

    def retranslateUi(self, ClientsTable):
        ClientsTable.setWindowTitle(QCoreApplication.translate("ClientsTable", u"Form", None))
    # retranslateUi


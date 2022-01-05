# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clients_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.clients.clients_table import ClientsTable


class Ui_ClientsPage(object):
    def setupUi(self, ClientsPage):
        if not ClientsPage.objectName():
            ClientsPage.setObjectName(u"ClientsPage")
        ClientsPage.resize(897, 581)
        self.verticalLayout_3 = QVBoxLayout(ClientsPage)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pageToolbar = QWidget(ClientsPage)
        self.pageToolbar.setObjectName(u"pageToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QSize(16777215, 40))
        self.headerLayout = QHBoxLayout(self.pageToolbar)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.pageToolbar)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.headerLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 40, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.headerLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addWidget(self.pageToolbar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(ClientsPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 20))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_2.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_4 = QLabel(ClientsPage)
        self.label_4.setObjectName(u"label_4")
        font2 = QFont()
        font2.setPointSize(12)
        self.label_4.setFont(font2)
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.clientsTable = ClientsTable(ClientsPage)
        self.clientsTable.setObjectName(u"clientsTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.clientsTable.sizePolicy().hasHeightForWidth())
        self.clientsTable.setSizePolicy(sizePolicy1)
        self.clientsTable.setMinimumSize(QSize(0, 200))
        self.clientsTable.setMaximumSize(QSize(16777215, 99999))

        self.verticalLayout.addWidget(self.clientsTable)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.chromeButton = QPushButton(ClientsPage)
        self.chromeButton.setObjectName(u"chromeButton")
        self.chromeButton.setEnabled(False)

        self.gridLayout.addWidget(self.chromeButton, 0, 0, 1, 1)

        self.chromiumButton = QPushButton(ClientsPage)
        self.chromiumButton.setObjectName(u"chromiumButton")
        self.chromiumButton.setEnabled(False)

        self.gridLayout.addWidget(self.chromiumButton, 0, 1, 1, 1)

        self.firefoxButton = QPushButton(ClientsPage)
        self.firefoxButton.setObjectName(u"firefoxButton")
        self.firefoxButton.setEnabled(False)

        self.gridLayout.addWidget(self.firefoxButton, 0, 2, 1, 1)

        self.terminalButton = QPushButton(ClientsPage)
        self.terminalButton.setObjectName(u"terminalButton")
        self.terminalButton.setEnabled(False)

        self.gridLayout.addWidget(self.terminalButton, 0, 3, 1, 1)

        self.existingTerminalButton = QPushButton(ClientsPage)
        self.existingTerminalButton.setObjectName(u"existingTerminalButton")
        self.existingTerminalButton.setEnabled(False)

        self.gridLayout.addWidget(self.existingTerminalButton, 0, 4, 1, 1)

        self.anythingButton = QPushButton(ClientsPage)
        self.anythingButton.setObjectName(u"anythingButton")
        self.anythingButton.setEnabled(False)

        self.gridLayout.addWidget(self.anythingButton, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 217, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.retranslateUi(ClientsPage)

        QMetaObject.connectSlotsByName(ClientsPage)
    # setupUi

    def retranslateUi(self, ClientsPage):
        ClientsPage.setWindowTitle(QCoreApplication.translate("ClientsPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("ClientsPage", u"CLIENTS", None))
        self.label_2.setText(QCoreApplication.translate("ClientsPage", u"Launch a Client", None))
        self.label_4.setText(QCoreApplication.translate("ClientsPage", u"To view and intercept HTTP(S) traffic, you need to launch a pre-configured and isolated client like a browser or a terminal session.\n"
"\n"
"Click an option below to start.", None))
        self.chromeButton.setText(QCoreApplication.translate("ClientsPage", u"Chrome", None))
        self.chromiumButton.setText(QCoreApplication.translate("ClientsPage", u"Chromium", None))
        self.firefoxButton.setText(QCoreApplication.translate("ClientsPage", u"Firefox", None))
        self.terminalButton.setText(QCoreApplication.translate("ClientsPage", u"Terminal", None))
        self.existingTerminalButton.setText(QCoreApplication.translate("ClientsPage", u"Existing Terminal", None))
        self.anythingButton.setText(QCoreApplication.translate("ClientsPage", u"Anything", None))
    # retranslateUi


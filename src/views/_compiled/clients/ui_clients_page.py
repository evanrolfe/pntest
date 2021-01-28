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
from widgets.clients.client_view import ClientView


class Ui_ClientsPage(object):
    def setupUi(self, ClientsPage):
        if not ClientsPage.objectName():
            ClientsPage.setObjectName(u"ClientsPage")
        ClientsPage.resize(897, 581)
        self.verticalLayout = QVBoxLayout(ClientsPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlerToolbar = QWidget(ClientsPage)
        self.crawlerToolbar.setObjectName(u"crawlerToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crawlerToolbar.sizePolicy().hasHeightForWidth())
        self.crawlerToolbar.setSizePolicy(sizePolicy)
        self.crawlerToolbar.setMaximumSize(QSize(16777215, 40))
        self.headerLayout = QHBoxLayout(self.crawlerToolbar)
        self.headerLayout.setObjectName(u"headerLayout")
        self.headerLayout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.crawlerToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.headerLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.headerLayout.addItem(self.horizontalSpacer)

        self.newClientButton = QPushButton(self.crawlerToolbar)
        self.newClientButton.setObjectName(u"newClientButton")
        self.newClientButton.setMaximumSize(QSize(100, 16777215))

        self.headerLayout.addWidget(self.newClientButton)


        self.verticalLayout.addWidget(self.crawlerToolbar)

        self.clientsSplitter = QSplitter(ClientsPage)
        self.clientsSplitter.setObjectName(u"clientsSplitter")
        self.clientsSplitter.setOrientation(Qt.Horizontal)
        self.clientsTable = ClientsTable(self.clientsSplitter)
        self.clientsTable.setObjectName(u"clientsTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.clientsTable.sizePolicy().hasHeightForWidth())
        self.clientsTable.setSizePolicy(sizePolicy1)
        self.clientsTable.setMinimumSize(QSize(350, 0))
        self.clientsSplitter.addWidget(self.clientsTable)
        self.clientView = ClientView(self.clientsSplitter)
        self.clientView.setObjectName(u"clientView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.clientView.sizePolicy().hasHeightForWidth())
        self.clientView.setSizePolicy(sizePolicy2)
        self.clientsSplitter.addWidget(self.clientView)

        self.verticalLayout.addWidget(self.clientsSplitter)


        self.retranslateUi(ClientsPage)

        QMetaObject.connectSlotsByName(ClientsPage)
    # setupUi

    def retranslateUi(self, ClientsPage):
        ClientsPage.setWindowTitle(QCoreApplication.translate("ClientsPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("ClientsPage", u"CLIENTS", None))
        self.newClientButton.setText(QCoreApplication.translate("ClientsPage", u"New Client", None))
    # retranslateUi


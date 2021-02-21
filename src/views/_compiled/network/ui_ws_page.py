# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ws_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.network.ws.messages_table import MessagesTable
from widgets.network.ws.message_view import MessageView


class Ui_WsPage(object):
    def setupUi(self, WsPage):
        if not WsPage.objectName():
            WsPage.setObjectName(u"WsPage")
        WsPage.resize(1400, 700)
        self.verticalLayout = QVBoxLayout(WsPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlerToolbar = QWidget(WsPage)
        self.crawlerToolbar.setObjectName(u"crawlerToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crawlerToolbar.sizePolicy().hasHeightForWidth())
        self.crawlerToolbar.setSizePolicy(sizePolicy)
        self.crawlerToolbar.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.crawlerToolbar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.crawlerToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toggleButton = QPushButton(self.crawlerToolbar)
        self.toggleButton.setObjectName(u"toggleButton")
        self.toggleButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.toggleButton)


        self.verticalLayout.addWidget(self.crawlerToolbar)

        self.messagesTableAndViewSplitter = QSplitter(WsPage)
        self.messagesTableAndViewSplitter.setObjectName(u"messagesTableAndViewSplitter")
        self.messagesTableAndViewSplitter.setOrientation(Qt.Horizontal)
        self.messagesTable = MessagesTable(self.messagesTableAndViewSplitter)
        self.messagesTable.setObjectName(u"messagesTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.messagesTable.sizePolicy().hasHeightForWidth())
        self.messagesTable.setSizePolicy(sizePolicy1)
        self.messagesTable.setMinimumSize(QSize(740, 0))
        self.messagesTableAndViewSplitter.addWidget(self.messagesTable)
        self.messageViewWidget = MessageView(self.messagesTableAndViewSplitter)
        self.messageViewWidget.setObjectName(u"messageViewWidget")
        sizePolicy1.setHeightForWidth(self.messageViewWidget.sizePolicy().hasHeightForWidth())
        self.messageViewWidget.setSizePolicy(sizePolicy1)
        self.messagesTableAndViewSplitter.addWidget(self.messageViewWidget)

        self.verticalLayout.addWidget(self.messagesTableAndViewSplitter)


        self.retranslateUi(WsPage)

        QMetaObject.connectSlotsByName(WsPage)
    # setupUi

    def retranslateUi(self, WsPage):
        WsPage.setWindowTitle(QCoreApplication.translate("WsPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("WsPage", u"NETWORK - WEBSOCKETS", None))
        self.toggleButton.setText(QCoreApplication.translate("WsPage", u"WS", None))
    # retranslateUi


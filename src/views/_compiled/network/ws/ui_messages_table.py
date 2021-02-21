# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'messages_table.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.qt.hoverable_q_table_view import HoverableQTableView


class Ui_MessagesTable(object):
    def setupUi(self, MessagesTable):
        if not MessagesTable.objectName():
            MessagesTable.setObjectName(u"MessagesTable")
        MessagesTable.resize(509, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MessagesTable.sizePolicy().hasHeightForWidth())
        MessagesTable.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(MessagesTable)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.searchBox = QLineEdit(MessagesTable)
        self.searchBox.setObjectName(u"searchBox")

        self.verticalLayout_2.addWidget(self.searchBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.displayFiltersButton = QPushButton(MessagesTable)
        self.displayFiltersButton.setObjectName(u"displayFiltersButton")

        self.horizontalLayout.addWidget(self.displayFiltersButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.messagesTable = HoverableQTableView(MessagesTable)
        self.messagesTable.setObjectName(u"messagesTable")

        self.verticalLayout_3.addWidget(self.messagesTable)


        self.retranslateUi(MessagesTable)

        QMetaObject.connectSlotsByName(MessagesTable)
    # setupUi

    def retranslateUi(self, MessagesTable):
        MessagesTable.setWindowTitle(QCoreApplication.translate("MessagesTable", u"Form", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("MessagesTable", u"Search", None))
        self.displayFiltersButton.setText(QCoreApplication.translate("MessagesTable", u"Display", None))
    # retranslateUi


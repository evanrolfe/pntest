# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'requests_table.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.qt.hoverable_q_table_view import HoverableQTableView


class Ui_RequestsTable(object):
    def setupUi(self, RequestsTable):
        if not RequestsTable.objectName():
            RequestsTable.setObjectName(u"RequestsTable")
        RequestsTable.resize(509, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RequestsTable.sizePolicy().hasHeightForWidth())
        RequestsTable.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(RequestsTable)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.searchBox = QLineEdit(RequestsTable)
        self.searchBox.setObjectName(u"searchBox")

        self.verticalLayout_2.addWidget(self.searchBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.displayFiltersButton = QPushButton(RequestsTable)
        self.displayFiltersButton.setObjectName(u"displayFiltersButton")
        self.displayFiltersButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.displayFiltersButton)

        self.captureFiltersButton = QPushButton(RequestsTable)
        self.captureFiltersButton.setObjectName(u"captureFiltersButton")
        self.captureFiltersButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.captureFiltersButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.requestsTable = HoverableQTableView(RequestsTable)
        self.requestsTable.setObjectName(u"requestsTable")

        self.verticalLayout_3.addWidget(self.requestsTable)


        self.retranslateUi(RequestsTable)

        QMetaObject.connectSlotsByName(RequestsTable)
    # setupUi

    def retranslateUi(self, RequestsTable):
        RequestsTable.setWindowTitle(QCoreApplication.translate("RequestsTable", u"Form", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("RequestsTable", u"Press enter to search", None))
        self.displayFiltersButton.setText(QCoreApplication.translate("RequestsTable", u"Display", None))
        self.captureFiltersButton.setText(QCoreApplication.translate("RequestsTable", u"Capture", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'http_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.network.http.requests_table import RequestsTable
from widgets.shared.request_view import RequestView


class Ui_HttpPage(object):
    def setupUi(self, HttpPage):
        if not HttpPage.objectName():
            HttpPage.setObjectName(u"HttpPage")
        HttpPage.resize(1400, 700)
        self.verticalLayout = QVBoxLayout(HttpPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlerToolbar = QWidget(HttpPage)
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

        self.newClientButton = QPushButton(self.crawlerToolbar)
        self.newClientButton.setObjectName(u"newClientButton")
        self.newClientButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.newClientButton)


        self.verticalLayout.addWidget(self.crawlerToolbar)

        self.requestsTableAndViewSplitter = QSplitter(HttpPage)
        self.requestsTableAndViewSplitter.setObjectName(u"requestsTableAndViewSplitter")
        self.requestsTableAndViewSplitter.setOrientation(Qt.Horizontal)
        self.requestsTableWidget = RequestsTable(self.requestsTableAndViewSplitter)
        self.requestsTableWidget.setObjectName(u"requestsTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.requestsTableWidget.sizePolicy().hasHeightForWidth())
        self.requestsTableWidget.setSizePolicy(sizePolicy1)
        self.requestsTableWidget.setMinimumSize(QSize(740, 0))
        self.requestsTableAndViewSplitter.addWidget(self.requestsTableWidget)
        self.requestViewWidget = RequestView(self.requestsTableAndViewSplitter)
        self.requestViewWidget.setObjectName(u"requestViewWidget")
        sizePolicy1.setHeightForWidth(self.requestViewWidget.sizePolicy().hasHeightForWidth())
        self.requestViewWidget.setSizePolicy(sizePolicy1)
        self.requestsTableAndViewSplitter.addWidget(self.requestViewWidget)

        self.verticalLayout.addWidget(self.requestsTableAndViewSplitter)


        self.retranslateUi(HttpPage)

        QMetaObject.connectSlotsByName(HttpPage)
    # setupUi

    def retranslateUi(self, HttpPage):
        HttpPage.setWindowTitle(QCoreApplication.translate("HttpPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("HttpPage", u"NETWORK", None))
        self.newClientButton.setText(QCoreApplication.translate("HttpPage", u"HTTP", None))
    # retranslateUi


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
from widgets.shared.flow_view import FlowView
from widgets.shared.loader import Loader


class Ui_HttpPage(object):
    def setupUi(self, HttpPage):
        if not HttpPage.objectName():
            HttpPage.setObjectName(u"HttpPage")
        HttpPage.resize(1400, 700)
        self.verticalLayout = QVBoxLayout(HttpPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pageToolbar = QWidget(HttpPage)
        self.pageToolbar.setObjectName(u"pageToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.pageToolbar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.pageToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toggleButton = QPushButton(self.pageToolbar)
        self.toggleButton.setObjectName(u"toggleButton")
        self.toggleButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.toggleButton)


        self.verticalLayout.addWidget(self.pageToolbar)

        self.requestsTableAndViewSplitter = QSplitter(HttpPage)
        self.requestsTableAndViewSplitter.setObjectName(u"requestsTableAndViewSplitter")
        self.requestsTableAndViewSplitter.setOrientation(Qt.Horizontal)
        self.stackedWidget = QStackedWidget(self.requestsTableAndViewSplitter)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.requestsTableWidget = RequestsTable()
        self.requestsTableWidget.setObjectName(u"requestsTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.requestsTableWidget.sizePolicy().hasHeightForWidth())
        self.requestsTableWidget.setSizePolicy(sizePolicy1)
        self.requestsTableWidget.setMinimumSize(QSize(740, 0))
        self.stackedWidget.addWidget(self.requestsTableWidget)
        self.loaderWidget = Loader()
        self.loaderWidget.setObjectName(u"loaderWidget")
        self.stackedWidget.addWidget(self.loaderWidget)
        self.requestsTableAndViewSplitter.addWidget(self.stackedWidget)
        self.requestViewWidget = FlowView(self.requestsTableAndViewSplitter)
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
        self.label.setText(QCoreApplication.translate("HttpPage", u"NETWORK - HTTP", None))
        self.toggleButton.setText(QCoreApplication.translate("HttpPage", u"WEBSOCKET", None))
    # retranslateUi


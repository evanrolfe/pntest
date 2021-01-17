# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_requests_table_tabs.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_RequestView(object):
    def setupUi(self, RequestView):
        if not RequestView.objectName():
            RequestView.setObjectName(u"RequestView")
        RequestView.resize(590, 678)
        self.verticalLayout_2 = QVBoxLayout(RequestView)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(RequestView)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.headerTabs = QTabWidget(self.splitter)
        self.headerTabs.setObjectName(u"headerTabs")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerTabs.sizePolicy().hasHeightForWidth())
        self.headerTabs.setSizePolicy(sizePolicy)
        self.httpTab = QWidget()
        self.httpTab.setObjectName(u"httpTab")
        self.verticalLayout_4 = QVBoxLayout(self.httpTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.requestHeadersText = QPlainTextEdit(self.httpTab)
        self.requestHeadersText.setObjectName(u"requestHeadersText")

        self.verticalLayout_4.addWidget(self.requestHeadersText)

        self.headerTabs.addTab(self.httpTab, "")
        self.wsTab = QWidget()
        self.wsTab.setObjectName(u"wsTab")
        self.wsTab.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.wsTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.requestHeadersModifiedText = QPlainTextEdit(self.wsTab)
        self.requestHeadersModifiedText.setObjectName(u"requestHeadersModifiedText")

        self.verticalLayout_3.addWidget(self.requestHeadersModifiedText)

        self.headerTabs.addTab(self.wsTab, "")
        self.splitter.addWidget(self.headerTabs)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(RequestView)

        self.headerTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestView)
    # setupUi

    def retranslateUi(self, RequestView):
        RequestView.setWindowTitle(QCoreApplication.translate("RequestView", u"Form", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.httpTab), QCoreApplication.translate("RequestView", u"HTTP", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.wsTab), QCoreApplication.translate("RequestView", u"WebSocket", None))
    # retranslateUi


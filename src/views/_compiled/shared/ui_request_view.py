# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_view.ui'
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

from PySide2.QtWebEngineWidgets import QWebEngineView


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
        self.requestTab = QWidget()
        self.requestTab.setObjectName(u"requestTab")
        self.verticalLayout_4 = QVBoxLayout(self.requestTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.requestHeadersText = QPlainTextEdit(self.requestTab)
        self.requestHeadersText.setObjectName(u"requestHeadersText")

        self.verticalLayout_4.addWidget(self.requestHeadersText)

        self.headerTabs.addTab(self.requestTab, "")
        self.requestModifiedTab = QWidget()
        self.requestModifiedTab.setObjectName(u"requestModifiedTab")
        self.requestModifiedTab.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.requestModifiedTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.requestHeadersModifiedText = QPlainTextEdit(self.requestModifiedTab)
        self.requestHeadersModifiedText.setObjectName(u"requestHeadersModifiedText")

        self.verticalLayout_3.addWidget(self.requestHeadersModifiedText)

        self.headerTabs.addTab(self.requestModifiedTab, "")
        self.responseTab = QWidget()
        self.responseTab.setObjectName(u"responseTab")
        self.verticalLayout = QVBoxLayout(self.responseTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.responseHeadersText = QPlainTextEdit(self.responseTab)
        self.responseHeadersText.setObjectName(u"responseHeadersText")

        self.verticalLayout.addWidget(self.responseHeadersText)

        self.headerTabs.addTab(self.responseTab, "")
        self.responseModifiedTab = QWidget()
        self.responseModifiedTab.setObjectName(u"responseModifiedTab")
        self.responseModifiedTab.setEnabled(True)
        self.verticalLayout_5 = QVBoxLayout(self.responseModifiedTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.responseHeadersModifiedText = QPlainTextEdit(self.responseModifiedTab)
        self.responseHeadersModifiedText.setObjectName(u"responseHeadersModifiedText")

        self.verticalLayout_5.addWidget(self.responseHeadersModifiedText)

        self.headerTabs.addTab(self.responseModifiedTab, "")
        self.splitter.addWidget(self.headerTabs)
        self.bodyTabs = QTabWidget(self.splitter)
        self.bodyTabs.setObjectName(u"bodyTabs")
        sizePolicy.setHeightForWidth(self.bodyTabs.sizePolicy().hasHeightForWidth())
        self.bodyTabs.setSizePolicy(sizePolicy)
        self.responseBodyRawTab = QWidget()
        self.responseBodyRawTab.setObjectName(u"responseBodyRawTab")
        self.verticalLayout_4_body = QVBoxLayout(self.responseBodyRawTab)
        self.verticalLayout_4_body.setObjectName(u"verticalLayout_4_body")
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyRawText = QPlainTextEdit(self.responseBodyRawTab)
        self.responseBodyRawText.setObjectName(u"responseBodyRawText")

        self.verticalLayout_4_body.addWidget(self.responseBodyRawText)

        self.bodyTabs.addTab(self.responseBodyRawTab, "")
        self.responseBodyModifiedTab = QWidget()
        self.responseBodyModifiedTab.setObjectName(u"responseBodyModifiedTab")
        self.responseBodyModifiedTab.setEnabled(True)
        self.verticalLayout_3_body = QVBoxLayout(self.responseBodyModifiedTab)
        self.verticalLayout_3_body.setObjectName(u"verticalLayout_3_body")
        self.verticalLayout_3_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyModifiedText = QPlainTextEdit(self.responseBodyModifiedTab)
        self.responseBodyModifiedText.setObjectName(u"responseBodyModifiedText")

        self.verticalLayout_3_body.addWidget(self.responseBodyModifiedText)

        self.bodyTabs.addTab(self.responseBodyModifiedTab, "")
        self.responseBodyParsedTab = QWidget()
        self.responseBodyParsedTab.setObjectName(u"responseBodyParsedTab")
        self.verticalLayout_body = QVBoxLayout(self.responseBodyParsedTab)
        self.verticalLayout_body.setSpacing(0)
        self.verticalLayout_body.setObjectName(u"verticalLayout_body")
        self.verticalLayout_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyParsedText = QPlainTextEdit(self.responseBodyParsedTab)
        self.responseBodyParsedText.setObjectName(u"responseBodyParsedText")

        self.verticalLayout_body.addWidget(self.responseBodyParsedText)

        self.bodyTabs.addTab(self.responseBodyParsedTab, "")
        self.responseBodyPreviewTab = QWidget()
        self.responseBodyPreviewTab.setObjectName(u"responseBodyPreviewTab")
        self.responseBodyPreviewTab.setEnabled(True)
        self.verticalLayout_5_body = QVBoxLayout(self.responseBodyPreviewTab)
        self.verticalLayout_5_body.setObjectName(u"verticalLayout_5_body")
        self.verticalLayout_5_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyPreview = QWebEngineView(self.responseBodyPreviewTab)
        self.responseBodyPreview.setObjectName(u"responseBodyPreview")

        self.verticalLayout_5_body.addWidget(self.responseBodyPreview)

        self.bodyTabs.addTab(self.responseBodyPreviewTab, "")
        self.splitter.addWidget(self.bodyTabs)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(RequestView)

        self.headerTabs.setCurrentIndex(3)
        self.bodyTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestView)
    # setupUi

    def retranslateUi(self, RequestView):
        RequestView.setWindowTitle(QCoreApplication.translate("RequestView", u"Form", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.requestTab), QCoreApplication.translate("RequestView", u"Request", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.requestModifiedTab), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.responseTab), QCoreApplication.translate("RequestView", u"Response", None))
        self.headerTabs.setTabText(self.headerTabs.indexOf(self.responseModifiedTab), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyRawTab), QCoreApplication.translate("RequestView", u"Raw", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyModifiedTab), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyParsedTab), QCoreApplication.translate("RequestView", u"Parsed", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyPreviewTab), QCoreApplication.translate("RequestView", u"Preview", None))
    # retranslateUi


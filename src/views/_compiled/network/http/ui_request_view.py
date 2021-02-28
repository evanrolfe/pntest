# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
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
        self.requestTabs = QTabWidget(self.splitter)
        self.requestTabs.setObjectName(u"requestTabs")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestTabs.sizePolicy().hasHeightForWidth())
        self.requestTabs.setSizePolicy(sizePolicy)
        self.requestTabs.setDocumentMode(False)
        self.splitter.addWidget(self.requestTabs)
        self.bodyTabs = QTabWidget(self.splitter)
        self.bodyTabs.setObjectName(u"bodyTabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.bodyTabs.sizePolicy().hasHeightForWidth())
        self.bodyTabs.setSizePolicy(sizePolicy1)
        self.responseBodyRawTab = QWidget()
        self.responseBodyRawTab.setObjectName(u"responseBodyRawTab")
        self.verticalLayout_4_body = QVBoxLayout(self.responseBodyRawTab)
        self.verticalLayout_4_body.setObjectName(u"verticalLayout_4_body")
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyRawCode = QWebEngineView(self.responseBodyRawTab)
        self.responseBodyRawCode.setObjectName(u"responseBodyRawCode")

        self.verticalLayout_4_body.addWidget(self.responseBodyRawCode)

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

        self.requestTabs.setCurrentIndex(-1)
        self.bodyTabs.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(RequestView)
    # setupUi

    def retranslateUi(self, RequestView):
        RequestView.setWindowTitle(QCoreApplication.translate("RequestView", u"Form", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyRawTab), QCoreApplication.translate("RequestView", u"Raw", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyModifiedTab), QCoreApplication.translate("RequestView", u"(Modified)", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyParsedTab), QCoreApplication.translate("RequestView", u"Parsed", None))
        self.bodyTabs.setTabText(self.bodyTabs.indexOf(self.responseBodyPreviewTab), QCoreApplication.translate("RequestView", u"Preview", None))
    # retranslateUi


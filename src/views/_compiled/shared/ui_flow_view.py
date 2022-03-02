# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'flow_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView
from widgets.shared.code_editor import CodeEditor
from widgets.shared.headers_form import HeadersForm
from widgets.shared.loader import Loader


class Ui_FlowView(object):
    def setupUi(self, FlowView):
        if not FlowView.objectName():
            FlowView.setObjectName(u"FlowView")
        FlowView.resize(590, 678)
        self.verticalLayout_2 = QVBoxLayout(FlowView)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(FlowView)
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
        self.requestHeadersTab = QWidget()
        self.requestHeadersTab.setObjectName(u"requestHeadersTab")
        self.verticalLayout_6_body = QVBoxLayout(self.requestHeadersTab)
        self.verticalLayout_6_body.setObjectName(u"verticalLayout_6_body")
        self.verticalLayout_6_body.setContentsMargins(0, 0, 0, 0)
        self.requestHeaders = HeadersForm(self.requestHeadersTab)
        self.requestHeaders.setObjectName(u"requestHeaders")

        self.verticalLayout_6_body.addWidget(self.requestHeaders)

        self.requestTabs.addTab(self.requestHeadersTab, "")
        self.requestBodyTab = QWidget()
        self.requestBodyTab.setObjectName(u"requestBodyTab")
        self.verticalLayout_7_body = QVBoxLayout(self.requestBodyTab)
        self.verticalLayout_7_body.setObjectName(u"verticalLayout_7_body")
        self.verticalLayout_7_body.setContentsMargins(0, 0, 0, 0)
        self.requestBody = CodeEditor(self.requestBodyTab)
        self.requestBody.setObjectName(u"requestBody")

        self.verticalLayout_7_body.addWidget(self.requestBody)

        self.requestTabs.addTab(self.requestBodyTab, "")
        self.splitter.addWidget(self.requestTabs)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.responseTabs = QTabWidget()
        self.responseTabs.setObjectName(u"responseTabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.responseTabs.sizePolicy().hasHeightForWidth())
        self.responseTabs.setSizePolicy(sizePolicy1)
        self.responseHeadersTab = QWidget()
        self.responseHeadersTab.setObjectName(u"responseHeadersTab")
        self.verticalLayout_8_body = QVBoxLayout(self.responseHeadersTab)
        self.verticalLayout_8_body.setObjectName(u"verticalLayout_8_body")
        self.verticalLayout_8_body.setContentsMargins(0, 0, 0, 0)
        self.responseHeaders = HeadersForm(self.responseHeadersTab)
        self.responseHeaders.setObjectName(u"responseHeaders")

        self.verticalLayout_8_body.addWidget(self.responseHeaders)

        self.responseTabs.addTab(self.responseHeadersTab, "")
        self.responseBodyRawTab = QWidget()
        self.responseBodyRawTab.setObjectName(u"responseBodyRawTab")
        self.verticalLayout_4_body = QVBoxLayout(self.responseBodyRawTab)
        self.verticalLayout_4_body.setObjectName(u"verticalLayout_4_body")
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.responseRaw = CodeEditor(self.responseBodyRawTab)
        self.responseRaw.setObjectName(u"responseRaw")

        self.verticalLayout_4_body.addWidget(self.responseRaw)

        self.responseTabs.addTab(self.responseBodyRawTab, "")
        self.responseBodyRenderedTab = QWidget()
        self.responseBodyRenderedTab.setObjectName(u"responseBodyRenderedTab")
        self.verticalLayout_body = QVBoxLayout(self.responseBodyRenderedTab)
        self.verticalLayout_body.setSpacing(0)
        self.verticalLayout_body.setObjectName(u"verticalLayout_body")
        self.verticalLayout_body.setContentsMargins(0, 0, 0, 0)
        self.responseRendered = CodeEditor(self.responseBodyRenderedTab)
        self.responseRendered.setObjectName(u"responseRendered")

        self.verticalLayout_body.addWidget(self.responseRendered)

        self.responseTabs.addTab(self.responseBodyRenderedTab, "")
        self.responseBodyPreviewTab = QWidget()
        self.responseBodyPreviewTab.setObjectName(u"responseBodyPreviewTab")
        self.responseBodyPreviewTab.setEnabled(True)
        self.verticalLayout_5_body = QVBoxLayout(self.responseBodyPreviewTab)
        self.verticalLayout_5_body.setObjectName(u"verticalLayout_5_body")
        self.verticalLayout_5_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyPreview = QWebEngineView(self.responseBodyPreviewTab)
        self.responseBodyPreview.setObjectName(u"responseBodyPreview")

        self.verticalLayout_5_body.addWidget(self.responseBodyPreview)

        self.responseTabs.addTab(self.responseBodyPreviewTab, "")
        self.stackedWidget.addWidget(self.responseTabs)
        self.loaderWidget = Loader()
        self.loaderWidget.setObjectName(u"loaderWidget")
        self.stackedWidget.addWidget(self.loaderWidget)
        self.splitter.addWidget(self.stackedWidget)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(FlowView)

        self.requestTabs.setCurrentIndex(1)
        self.responseTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(FlowView)
    # setupUi

    def retranslateUi(self, FlowView):
        FlowView.setWindowTitle(QCoreApplication.translate("FlowView", u"Form", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestHeadersTab), QCoreApplication.translate("FlowView", u"Request", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestBodyTab), QCoreApplication.translate("FlowView", u"Body", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseHeadersTab), QCoreApplication.translate("FlowView", u"Response", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyRawTab), QCoreApplication.translate("FlowView", u"Body", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyRenderedTab), QCoreApplication.translate("FlowView", u"Rendered", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyPreviewTab), QCoreApplication.translate("FlowView", u"Preview", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fuzz_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.shared.code_editor import CodeEditor
from widgets.shared.headers_form import HeadersForm
from widgets.shared.loader import Loader


class Ui_FuzzView(object):
    def setupUi(self, FuzzView):
        if not FuzzView.objectName():
            FuzzView.setObjectName(u"FuzzView")
        FuzzView.resize(658, 678)
        self.verticalLayout = QVBoxLayout(FuzzView)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(FuzzView)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.requestTabs = QTabWidget()
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
        self.fuzzPayloadsTab = QWidget()
        self.fuzzPayloadsTab.setObjectName(u"fuzzPayloadsTab")
        self.verticalLayout_8_body = QVBoxLayout(self.fuzzPayloadsTab)
        self.verticalLayout_8_body.setObjectName(u"verticalLayout_8_body")
        self.verticalLayout_8_body.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, -1)
        self.label = QLabel(self.fuzzPayloadsTab)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.addPayloadButton = QPushButton(self.fuzzPayloadsTab)
        self.addPayloadButton.setObjectName(u"addPayloadButton")

        self.horizontalLayout.addWidget(self.addPayloadButton)


        self.verticalLayout_8_body.addLayout(self.horizontalLayout)

        self.payloadsTable = QTableView(self.fuzzPayloadsTab)
        self.payloadsTable.setObjectName(u"payloadsTable")

        self.verticalLayout_8_body.addWidget(self.payloadsTable)

        self.requestTabs.addTab(self.fuzzPayloadsTab, "")
        self.stackedWidget.addWidget(self.requestTabs)
        self.loaderWidget = Loader()
        self.loaderWidget.setObjectName(u"loaderWidget")
        self.stackedWidget.addWidget(self.loaderWidget)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(FuzzView)

        self.stackedWidget.setCurrentIndex(0)
        self.requestTabs.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(FuzzView)
    # setupUi

    def retranslateUi(self, FuzzView):
        FuzzView.setWindowTitle(QCoreApplication.translate("FuzzView", u"Form", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestHeadersTab), QCoreApplication.translate("FuzzView", u"Request", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestBodyTab), QCoreApplication.translate("FuzzView", u"Body", None))
        self.label.setText(QCoreApplication.translate("FuzzView", u"Payloads", None))
        self.addPayloadButton.setText(QCoreApplication.translate("FuzzView", u"Import Payload", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.fuzzPayloadsTab), QCoreApplication.translate("FuzzView", u"Fuzzing Payloads", None))
    # retranslateUi


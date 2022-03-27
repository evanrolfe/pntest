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
        self.verticalLayout_8_body.setContentsMargins(0, 0, 0, 10)
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

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, -1)
        self.label_2 = QLabel(self.fuzzPayloadsTab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.fuzzTypeDropdown = QComboBox(self.fuzzPayloadsTab)
        self.fuzzTypeDropdown.setObjectName(u"fuzzTypeDropdown")

        self.horizontalLayout_2.addWidget(self.fuzzTypeDropdown)


        self.verticalLayout_8_body.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, -1)
        self.label_3 = QLabel(self.fuzzPayloadsTab)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.comboBox = QComboBox(self.fuzzPayloadsTab)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)


        self.verticalLayout_8_body.addLayout(self.horizontalLayout_3)

        self.hlayout_4 = QHBoxLayout()
        self.hlayout_4.setObjectName(u"hlayout_4")
        self.hlayout_4.setContentsMargins(10, 10, 10, -1)
        self.label_4 = QLabel(self.fuzzPayloadsTab)
        self.label_4.setObjectName(u"label_4")

        self.hlayout_4.addWidget(self.label_4)

        self.delayDuration = QLineEdit(self.fuzzPayloadsTab)
        self.delayDuration.setObjectName(u"delayDuration")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.delayDuration.sizePolicy().hasHeightForWidth())
        self.delayDuration.setSizePolicy(sizePolicy1)
        self.delayDuration.setMaximumSize(QSize(50, 16777215))

        self.hlayout_4.addWidget(self.delayDuration)


        self.verticalLayout_8_body.addLayout(self.hlayout_4)

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
        self.label_2.setText(QCoreApplication.translate("FuzzView", u"Fuzzing Type", None))
        self.label_3.setText(QCoreApplication.translate("FuzzView", u"Delay Type", None))
        self.label_4.setText(QCoreApplication.translate("FuzzView", u"Delay Duration", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.fuzzPayloadsTab), QCoreApplication.translate("FuzzView", u"Fuzzing Options", None))
    # retranslateUi


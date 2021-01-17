# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_edit_page.ui'
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


class Ui_RequestEditPage(object):
    def setupUi(self, RequestEditPage):
        if not RequestEditPage.objectName():
            RequestEditPage.setObjectName(u"RequestEditPage")
        RequestEditPage.resize(897, 581)
        self.verticalLayout_2 = QVBoxLayout(RequestEditPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.requestEditSplitter = QSplitter(RequestEditPage)
        self.requestEditSplitter.setObjectName(u"requestEditSplitter")
        self.requestEditSplitter.setOrientation(Qt.Horizontal)
        self.fuzzRequestsTable = QTableView(self.requestEditSplitter)
        self.fuzzRequestsTable.setObjectName(u"fuzzRequestsTable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuzzRequestsTable.sizePolicy().hasHeightForWidth())
        self.fuzzRequestsTable.setSizePolicy(sizePolicy)
        self.requestEditSplitter.addWidget(self.fuzzRequestsTable)
        self.splitter2 = QSplitter(self.requestEditSplitter)
        self.splitter2.setObjectName(u"splitter2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(2)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter2.sizePolicy().hasHeightForWidth())
        self.splitter2.setSizePolicy(sizePolicy1)
        self.splitter2.setOrientation(Qt.Vertical)
        self.layoutWidget = QWidget(self.splitter2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.layout1 = QHBoxLayout()
        self.layout1.setObjectName(u"layout1")
        self.layout1.setContentsMargins(10, 10, 10, -1)
        self.toggleFuzzTableButton = QPushButton(self.layoutWidget)
        self.toggleFuzzTableButton.setObjectName(u"toggleFuzzTableButton")
        self.toggleFuzzTableButton.setMaximumSize(QSize(35, 16777215))

        self.layout1.addWidget(self.toggleFuzzTableButton)

        self.horizontalSpacer = QSpacerItem(388, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout1.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.layout1)

        self.requestActionsLayout = QHBoxLayout()
        self.requestActionsLayout.setObjectName(u"requestActionsLayout")
        self.requestActionsLayout.setContentsMargins(10, 10, 10, 10)
        self.methodInput = QComboBox(self.layoutWidget)
        self.methodInput.setObjectName(u"methodInput")

        self.requestActionsLayout.addWidget(self.methodInput)

        self.urlInput = QLineEdit(self.layoutWidget)
        self.urlInput.setObjectName(u"urlInput")
        self.urlInput.setMinimumSize(QSize(300, 0))

        self.requestActionsLayout.addWidget(self.urlInput)

        self.sendButton = QPushButton(self.layoutWidget)
        self.sendButton.setObjectName(u"sendButton")

        self.requestActionsLayout.addWidget(self.sendButton)

        self.saveButton = QPushButton(self.layoutWidget)
        self.saveButton.setObjectName(u"saveButton")

        self.requestActionsLayout.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.requestActionsLayout)

        self.requestTabs = QTabWidget(self.layoutWidget)
        self.requestTabs.setObjectName(u"requestTabs")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.requestTabs.sizePolicy().hasHeightForWidth())
        self.requestTabs.setSizePolicy(sizePolicy2)
        self.requestTabs.setDocumentMode(False)

        self.verticalLayout.addWidget(self.requestTabs)

        self.splitter2.addWidget(self.layoutWidget)
        self.responseTabs = QTabWidget(self.splitter2)
        self.responseTabs.setObjectName(u"responseTabs")
        sizePolicy2.setHeightForWidth(self.responseTabs.sizePolicy().hasHeightForWidth())
        self.responseTabs.setSizePolicy(sizePolicy2)
        self.responseBodyTab = QWidget()
        self.responseBodyTab.setObjectName(u"responseBodyTab")
        self.verticalLayout_4_body = QVBoxLayout(self.responseBodyTab)
        self.verticalLayout_4_body.setObjectName(u"verticalLayout_4_body")
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.responseBodyText = QPlainTextEdit(self.responseBodyTab)
        self.responseBodyText.setObjectName(u"responseBodyText")

        self.verticalLayout_4_body.addWidget(self.responseBodyText)

        self.responseTabs.addTab(self.responseBodyTab, "")
        self.responseHeadersTab = QWidget()
        self.responseHeadersTab.setObjectName(u"responseHeadersTab")
        self.verticalLayout_4_body2 = QVBoxLayout(self.responseHeadersTab)
        self.verticalLayout_4_body2.setObjectName(u"verticalLayout_4_body2")
        self.verticalLayout_4_body2.setContentsMargins(0, 0, 0, 0)
        self.responseHeadersText = QPlainTextEdit(self.responseHeadersTab)
        self.responseHeadersText.setObjectName(u"responseHeadersText")

        self.verticalLayout_4_body2.addWidget(self.responseHeadersText)

        self.responseTabs.addTab(self.responseHeadersTab, "")
        self.splitter2.addWidget(self.responseTabs)
        self.requestEditSplitter.addWidget(self.splitter2)

        self.verticalLayout_2.addWidget(self.requestEditSplitter)


        self.retranslateUi(RequestEditPage)

        self.requestTabs.setCurrentIndex(-1)
        self.responseTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestEditPage)
    # setupUi

    def retranslateUi(self, RequestEditPage):
        RequestEditPage.setWindowTitle(QCoreApplication.translate("RequestEditPage", u"Form", None))
        self.toggleFuzzTableButton.setText(QCoreApplication.translate("RequestEditPage", u"<<", None))
        self.sendButton.setText(QCoreApplication.translate("RequestEditPage", u"Send", None))
        self.saveButton.setText(QCoreApplication.translate("RequestEditPage", u"Save", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyTab), QCoreApplication.translate("RequestEditPage", u"Response", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseHeadersTab), QCoreApplication.translate("RequestEditPage", u"Headers", None))
    # retranslateUi


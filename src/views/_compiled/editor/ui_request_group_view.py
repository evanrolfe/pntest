# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_group_view.ui'
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


class Ui_RequestGroupView(object):
    def setupUi(self, RequestGroupView):
        if not RequestGroupView.objectName():
            RequestGroupView.setObjectName(u"RequestGroupView")
        RequestGroupView.resize(897, 581)
        self.verticalLayout_2 = QVBoxLayout(RequestGroupView)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(RequestGroupView)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.fuzzRequestsTable = QTableView(self.splitter)
        self.fuzzRequestsTable.setObjectName(u"fuzzRequestsTable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuzzRequestsTable.sizePolicy().hasHeightForWidth())
        self.fuzzRequestsTable.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.fuzzRequestsTable)
        self.splitter2 = QSplitter(self.splitter)
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
        self.requestActionsLayout = QHBoxLayout()
        self.requestActionsLayout.setObjectName(u"requestActionsLayout")
        self.requestActionsLayout.setContentsMargins(0, 5, 5, -1)
        self.toggleFuzzTableButton = QPushButton(self.layoutWidget)
        self.toggleFuzzTableButton.setObjectName(u"toggleFuzzTableButton")
        self.toggleFuzzTableButton.setMaximumSize(QSize(35, 16777215))

        self.requestActionsLayout.addWidget(self.toggleFuzzTableButton)

        self.comboBox = QComboBox(self.layoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.requestActionsLayout.addWidget(self.comboBox)

        self.urlInput = QLineEdit(self.layoutWidget)
        self.urlInput.setObjectName(u"urlInput")
        self.urlInput.setMinimumSize(QSize(300, 0))

        self.requestActionsLayout.addWidget(self.urlInput)

        self.sendRequestButton = QPushButton(self.layoutWidget)
        self.sendRequestButton.setObjectName(u"sendRequestButton")

        self.requestActionsLayout.addWidget(self.sendRequestButton)

        self.saveRequestButton = QPushButton(self.layoutWidget)
        self.saveRequestButton.setObjectName(u"saveRequestButton")

        self.requestActionsLayout.addWidget(self.saveRequestButton)


        self.verticalLayout.addLayout(self.requestActionsLayout)

        self.requestTabs = QTabWidget(self.layoutWidget)
        self.requestTabs.setObjectName(u"requestTabs")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.requestTabs.sizePolicy().hasHeightForWidth())
        self.requestTabs.setSizePolicy(sizePolicy2)
        self.requestTab = QWidget()
        self.requestTab.setObjectName(u"requestTab")
        self.verticalLayout_4 = QVBoxLayout(self.requestTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.requestText = QPlainTextEdit(self.requestTab)
        self.requestText.setObjectName(u"requestText")

        self.verticalLayout_4.addWidget(self.requestText)

        self.requestTabs.addTab(self.requestTab, "")

        self.verticalLayout.addWidget(self.requestTabs)

        self.splitter2.addWidget(self.layoutWidget)
        self.responseTabs = QTabWidget(self.splitter2)
        self.responseTabs.setObjectName(u"responseTabs")
        sizePolicy2.setHeightForWidth(self.responseTabs.sizePolicy().hasHeightForWidth())
        self.responseTabs.setSizePolicy(sizePolicy2)
        self.responseTab = QWidget()
        self.responseTab.setObjectName(u"responseTab")
        self.verticalLayout_4_body = QVBoxLayout(self.responseTab)
        self.verticalLayout_4_body.setObjectName(u"verticalLayout_4_body")
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.responseText = QPlainTextEdit(self.responseTab)
        self.responseText.setObjectName(u"responseText")

        self.verticalLayout_4_body.addWidget(self.responseText)

        self.responseTabs.addTab(self.responseTab, "")
        self.responseBodyTab = QWidget()
        self.responseBodyTab.setObjectName(u"responseBodyTab")
        self.responseBodyTab.setEnabled(True)
        self.responseBodyText = QPlainTextEdit(self.responseBodyTab)
        self.responseBodyText.setObjectName(u"responseBodyText")
        self.responseBodyText.setGeometry(QRect(0, 0, 256, 192))
        self.responseTabs.addTab(self.responseBodyTab, "")
        self.splitter2.addWidget(self.responseTabs)
        self.splitter.addWidget(self.splitter2)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(RequestGroupView)

        self.requestTabs.setCurrentIndex(0)
        self.responseTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestGroupView)
    # setupUi

    def retranslateUi(self, RequestGroupView):
        RequestGroupView.setWindowTitle(QCoreApplication.translate("RequestGroupView", u"Form", None))
        self.toggleFuzzTableButton.setText(QCoreApplication.translate("RequestGroupView", u"<<", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("RequestGroupView", u"GET", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("RequestGroupView", u"POST", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("RequestGroupView", u"PATCH", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("RequestGroupView", u"PUT", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("RequestGroupView", u"DELETE", None))

        self.sendRequestButton.setText(QCoreApplication.translate("RequestGroupView", u"Send", None))
        self.saveRequestButton.setText(QCoreApplication.translate("RequestGroupView", u"Save", None))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestTab), QCoreApplication.translate("RequestGroupView", u"Request", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseTab), QCoreApplication.translate("RequestGroupView", u"Response", None))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyTab), QCoreApplication.translate("RequestGroupView", u"Body", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_edit_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.shared.request_view import RequestView


class Ui_RequestEditPage(object):
    def setupUi(self, RequestEditPage):
        if not RequestEditPage.objectName():
            RequestEditPage.setObjectName(u"RequestEditPage")
        RequestEditPage.resize(897, 581)
        self.horizontalLayout = QHBoxLayout(RequestEditPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fuzzRequestsTable = QTableView(RequestEditPage)
        self.fuzzRequestsTable.setObjectName(u"fuzzRequestsTable")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuzzRequestsTable.sizePolicy().hasHeightForWidth())
        self.fuzzRequestsTable.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.fuzzRequestsTable)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout1 = QHBoxLayout()
        self.layout1.setObjectName(u"layout1")
        self.layout1.setContentsMargins(10, 10, 10, -1)
        self.horizontalSpacer = QSpacerItem(388, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout1.addItem(self.horizontalSpacer)

        self.toggleFuzzTableButton = QPushButton(RequestEditPage)
        self.toggleFuzzTableButton.setObjectName(u"toggleFuzzTableButton")

        self.layout1.addWidget(self.toggleFuzzTableButton)


        self.verticalLayout.addLayout(self.layout1)

        self.requestActionsLayout = QHBoxLayout()
        self.requestActionsLayout.setObjectName(u"requestActionsLayout")
        self.requestActionsLayout.setContentsMargins(10, 10, 10, 20)
        self.methodInput = QComboBox(RequestEditPage)
        self.methodInput.setObjectName(u"methodInput")

        self.requestActionsLayout.addWidget(self.methodInput)

        self.urlInput = QLineEdit(RequestEditPage)
        self.urlInput.setObjectName(u"urlInput")
        self.urlInput.setMinimumSize(QSize(300, 0))

        self.requestActionsLayout.addWidget(self.urlInput)

        self.sendButton = QPushButton(RequestEditPage)
        self.sendButton.setObjectName(u"sendButton")

        self.requestActionsLayout.addWidget(self.sendButton)

        self.saveButton = QPushButton(RequestEditPage)
        self.saveButton.setObjectName(u"saveButton")

        self.requestActionsLayout.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.requestActionsLayout)

        self.layout2 = QHBoxLayout()
        self.layout2.setObjectName(u"layout2")
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.requestViewWidget = RequestView(RequestEditPage)
        self.requestViewWidget.setObjectName(u"requestViewWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.requestViewWidget.sizePolicy().hasHeightForWidth())
        self.requestViewWidget.setSizePolicy(sizePolicy1)

        self.layout2.addWidget(self.requestViewWidget)


        self.verticalLayout.addLayout(self.layout2)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(RequestEditPage)

        QMetaObject.connectSlotsByName(RequestEditPage)
    # setupUi

    def retranslateUi(self, RequestEditPage):
        RequestEditPage.setWindowTitle(QCoreApplication.translate("RequestEditPage", u"Form", None))
        self.toggleFuzzTableButton.setText(QCoreApplication.translate("RequestEditPage", u"Saved Examples (10) <<", None))
        self.sendButton.setText(QCoreApplication.translate("RequestEditPage", u"Send", None))
        self.saveButton.setText(QCoreApplication.translate("RequestEditPage", u"Save", None))
    # retranslateUi


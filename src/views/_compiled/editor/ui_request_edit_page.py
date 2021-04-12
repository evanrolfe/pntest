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

from widgets.shared.flow_view import FlowView
from widgets.editor.examples_table import ExamplesTable


class Ui_RequestEditPage(object):
    def setupUi(self, RequestEditPage):
        if not RequestEditPage.objectName():
            RequestEditPage.setObjectName(u"RequestEditPage")
        RequestEditPage.resize(897, 581)
        self.horizontalLayout = QHBoxLayout(RequestEditPage)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.requestEditSplitter = QSplitter(RequestEditPage)
        self.requestEditSplitter.setObjectName(u"requestEditSplitter")
        self.requestEditSplitter.setOrientation(Qt.Horizontal)
        self.examplesTable = ExamplesTable(self.requestEditSplitter)
        self.examplesTable.setObjectName(u"examplesTable")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.examplesTable.sizePolicy().hasHeightForWidth())
        self.examplesTable.setSizePolicy(sizePolicy)
        self.examplesTable.setMinimumSize(QSize(0, 200))
        self.examplesTable.setMaximumSize(QSize(16777215, 99999))
        self.requestEditSplitter.addWidget(self.examplesTable)
        self.layoutWidget = QWidget(self.requestEditSplitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.layout1 = QHBoxLayout()
        self.layout1.setObjectName(u"layout1")
        self.layout1.setContentsMargins(10, 10, 10, -1)
        self.toggleExamplesButton = QPushButton(self.layoutWidget)
        self.toggleExamplesButton.setObjectName(u"toggleExamplesButton")

        self.layout1.addWidget(self.toggleExamplesButton)

        self.horizontalSpacer = QSpacerItem(388, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout1.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.layout1)

        self.requestActionsLayout = QHBoxLayout()
        self.requestActionsLayout.setObjectName(u"requestActionsLayout")
        self.requestActionsLayout.setContentsMargins(10, 10, 10, 20)
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

        self.layout2 = QHBoxLayout()
        self.layout2.setObjectName(u"layout2")
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.flowView = FlowView(self.layoutWidget)
        self.flowView.setObjectName(u"flowView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.flowView.sizePolicy().hasHeightForWidth())
        self.flowView.setSizePolicy(sizePolicy1)

        self.layout2.addWidget(self.flowView)


        self.verticalLayout.addLayout(self.layout2)

        self.requestEditSplitter.addWidget(self.layoutWidget)

        self.horizontalLayout.addWidget(self.requestEditSplitter)


        self.retranslateUi(RequestEditPage)

        QMetaObject.connectSlotsByName(RequestEditPage)
    # setupUi

    def retranslateUi(self, RequestEditPage):
        RequestEditPage.setWindowTitle(QCoreApplication.translate("RequestEditPage", u"Form", None))
        self.toggleExamplesButton.setText(QCoreApplication.translate("RequestEditPage", u"Saved Examples (10) <<", None))
        self.sendButton.setText(QCoreApplication.translate("RequestEditPage", u"Send", None))
        self.saveButton.setText(QCoreApplication.translate("RequestEditPage", u"Save", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'message_view.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MessageView(object):
    def setupUi(self, MessageView):
        if not MessageView.objectName():
            MessageView.setObjectName(u"MessageView")
        MessageView.resize(590, 678)
        self.verticalLayout_2 = QVBoxLayout(MessageView)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(MessageView)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.messageTabs = QTabWidget(self.splitter)
        self.messageTabs.setObjectName(u"messageTabs")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageTabs.sizePolicy().hasHeightForWidth())
        self.messageTabs.setSizePolicy(sizePolicy)
        self.messageTab = QWidget()
        self.messageTab.setObjectName(u"messageTab")
        self.verticalLayout_4 = QVBoxLayout(self.messageTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.messageText = QPlainTextEdit(self.messageTab)
        self.messageText.setObjectName(u"messageText")

        self.verticalLayout_4.addWidget(self.messageText)

        self.messageTabs.addTab(self.messageTab, "")
        self.messageModifiedTab = QWidget()
        self.messageModifiedTab.setObjectName(u"messageModifiedTab")
        self.messageModifiedTab.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.messageModifiedTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.messageModifiedText = QPlainTextEdit(self.messageModifiedTab)
        self.messageModifiedText.setObjectName(u"messageModifiedText")

        self.verticalLayout_3.addWidget(self.messageModifiedText)

        self.messageTabs.addTab(self.messageModifiedTab, "")
        self.splitter.addWidget(self.messageTabs)

        self.verticalLayout_2.addWidget(self.splitter)


        self.retranslateUi(MessageView)

        self.messageTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MessageView)
    # setupUi

    def retranslateUi(self, MessageView):
        MessageView.setWindowTitle(QCoreApplication.translate("MessageView", u"Form", None))
        self.messageTabs.setTabText(self.messageTabs.indexOf(self.messageTab), QCoreApplication.translate("MessageView", u"Message", None))
        self.messageTabs.setTabText(self.messageTabs.indexOf(self.messageModifiedTab), QCoreApplication.translate("MessageView", u"(Modified)", None))
    # retranslateUi


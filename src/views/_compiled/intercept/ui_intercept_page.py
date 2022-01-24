# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'intercept_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.shared.headers_form import HeadersForm


class Ui_InterceptPage(object):
    def setupUi(self, InterceptPage):
        if not InterceptPage.objectName():
            InterceptPage.setObjectName(u"InterceptPage")
        InterceptPage.resize(897, 581)
        self.verticalLayout = QVBoxLayout(InterceptPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pageToolbar = QWidget(InterceptPage)
        self.pageToolbar.setObjectName(u"pageToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.pageToolbar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.pageToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 40, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.pageToolbar)

        self.interceptedRequestLayout = QVBoxLayout()
        self.interceptedRequestLayout.setObjectName(u"interceptedRequestLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 5, 10, 15)
        self.interceptTitle = QLabel(InterceptPage)
        self.interceptTitle.setObjectName(u"interceptTitle")
        font1 = QFont()
        font1.setBold(False)
        font1.setWeight(50)
        self.interceptTitle.setFont(font1)

        self.verticalLayout_2.addWidget(self.interceptTitle)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setSpacing(6)
        self.horizontalLayout2.setObjectName(u"horizontalLayout2")
        self.forwardButton = QPushButton(InterceptPage)
        self.forwardButton.setObjectName(u"forwardButton")
        self.forwardButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout2.addWidget(self.forwardButton)

        self.forwardInterceptButton = QPushButton(InterceptPage)
        self.forwardInterceptButton.setObjectName(u"forwardInterceptButton")
        self.forwardInterceptButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout2.addWidget(self.forwardInterceptButton)

        self.dropButton = QPushButton(InterceptPage)
        self.dropButton.setObjectName(u"dropButton")
        self.dropButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout2.addWidget(self.dropButton)

        self.enabledButton = QPushButton(InterceptPage)
        self.enabledButton.setObjectName(u"enabledButton")
        self.enabledButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout2.addWidget(self.enabledButton)

        self.horizontalSpacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout2.addItem(self.horizontalSpacer2)


        self.verticalLayout_2.addLayout(self.horizontalLayout2)


        self.interceptedRequestLayout.addLayout(self.verticalLayout_2)

        self.interceptTabs = QTabWidget(InterceptPage)
        self.interceptTabs.setObjectName(u"interceptTabs")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.interceptTabs.sizePolicy().hasHeightForWidth())
        self.interceptTabs.setSizePolicy(sizePolicy1)
        self.headersTab = QWidget()
        self.headersTab.setObjectName(u"headersTab")
        self.verticalLayout_4 = QVBoxLayout(self.headersTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.headers = HeadersForm(self.headersTab)
        self.headers.setObjectName(u"headers")

        self.verticalLayout_4.addWidget(self.headers)

        self.interceptTabs.addTab(self.headersTab, "")
        self.bodyTab = QWidget()
        self.bodyTab.setObjectName(u"bodyTab")
        self.verticalLayout5 = QVBoxLayout(self.bodyTab)
        self.verticalLayout5.setSpacing(0)
        self.verticalLayout5.setObjectName(u"verticalLayout5")
        self.verticalLayout5.setContentsMargins(0, 0, 0, 0)
        self.bodyText = QPlainTextEdit(self.bodyTab)
        self.bodyText.setObjectName(u"bodyText")

        self.verticalLayout5.addWidget(self.bodyText)

        self.interceptTabs.addTab(self.bodyTab, "")

        self.interceptedRequestLayout.addWidget(self.interceptTabs)


        self.verticalLayout.addLayout(self.interceptedRequestLayout)


        self.retranslateUi(InterceptPage)

        self.interceptTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(InterceptPage)
    # setupUi

    def retranslateUi(self, InterceptPage):
        InterceptPage.setWindowTitle(QCoreApplication.translate("InterceptPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("InterceptPage", u"INTERCEPT", None))
        self.interceptTitle.setText(QCoreApplication.translate("InterceptPage", u"Intercepted Request:", None))
        self.forwardButton.setText(QCoreApplication.translate("InterceptPage", u"Forward", None))
        self.forwardInterceptButton.setText(QCoreApplication.translate("InterceptPage", u"Forward + Intercept Response", None))
        self.dropButton.setText(QCoreApplication.translate("InterceptPage", u"Drop", None))
        self.enabledButton.setText(QCoreApplication.translate("InterceptPage", u"Enable Intercept", None))
        self.interceptTabs.setTabText(self.interceptTabs.indexOf(self.headersTab), QCoreApplication.translate("InterceptPage", u"Headers", None))
        self.interceptTabs.setTabText(self.interceptTabs.indexOf(self.bodyTab), QCoreApplication.translate("InterceptPage", u"Body", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'intercept_page.ui'
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


class Ui_InterceptPage(object):
    def setupUi(self, InterceptPage):
        if not InterceptPage.objectName():
            InterceptPage.setObjectName(u"InterceptPage")
        InterceptPage.resize(741, 511)
        self.verticalLayout_5 = QVBoxLayout(InterceptPage)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.crawlerToolbar = QWidget(InterceptPage)
        self.crawlerToolbar.setObjectName(u"crawlerToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crawlerToolbar.sizePolicy().hasHeightForWidth())
        self.crawlerToolbar.setSizePolicy(sizePolicy)
        self.crawlerToolbar.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout = QHBoxLayout(self.crawlerToolbar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.crawlerToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addWidget(self.crawlerToolbar)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.interceptTitle = QLabel(InterceptPage)
        self.interceptTitle.setObjectName(u"interceptTitle")
        font1 = QFont()
        font1.setBold(False)
        font1.setWeight(50)
        self.interceptTitle.setFont(font1)

        self.verticalLayout_2.addWidget(self.interceptTitle)

        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setObjectName(u"horizontalLayout1")
        self.forwardButton = QPushButton(InterceptPage)
        self.forwardButton.setObjectName(u"forwardButton")

        self.horizontalLayout1.addWidget(self.forwardButton)

        self.forwardInterceptButton = QPushButton(InterceptPage)
        self.forwardInterceptButton.setObjectName(u"forwardInterceptButton")

        self.horizontalLayout1.addWidget(self.forwardInterceptButton)

        self.dropButton = QPushButton(InterceptPage)
        self.dropButton.setObjectName(u"dropButton")

        self.horizontalLayout1.addWidget(self.dropButton)

        self.enabledButton = QPushButton(InterceptPage)
        self.enabledButton.setObjectName(u"enabledButton")

        self.horizontalLayout1.addWidget(self.enabledButton)

        self.horizontalSpacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout1.addItem(self.horizontalSpacer1)


        self.verticalLayout_2.addLayout(self.horizontalLayout1)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

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
        self.headersText = QPlainTextEdit(self.headersTab)
        self.headersText.setObjectName(u"headersText")

        self.verticalLayout_4.addWidget(self.headersText)

        self.interceptTabs.addTab(self.headersTab, "")
        self.bodyTab = QWidget()
        self.bodyTab.setObjectName(u"bodyTab")
        self.verticalLayout = QVBoxLayout(self.bodyTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bodyText = QPlainTextEdit(self.bodyTab)
        self.bodyText.setObjectName(u"bodyText")

        self.verticalLayout.addWidget(self.bodyText)

        self.interceptTabs.addTab(self.bodyTab, "")

        self.verticalLayout_3.addWidget(self.interceptTabs)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)


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


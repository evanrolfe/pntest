# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_crawl.ui'
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


class Ui_NewCrawl(object):
    def setupUi(self, NewCrawl):
        if not NewCrawl.objectName():
            NewCrawl.setObjectName(u"NewCrawl")
        NewCrawl.resize(638, 449)
        self.verticalLayout = QVBoxLayout(NewCrawl)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(NewCrawl)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.clientsDropdown = QComboBox(NewCrawl)
        self.clientsDropdown.addItem("")
        self.clientsDropdown.addItem("")
        self.clientsDropdown.addItem("")
        self.clientsDropdown.setObjectName(u"clientsDropdown")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clientsDropdown.sizePolicy().hasHeightForWidth())
        self.clientsDropdown.setSizePolicy(sizePolicy)
        self.clientsDropdown.setMinimumSize(QSize(205, 0))

        self.horizontalLayout.addWidget(self.clientsDropdown)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(NewCrawl)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.label_5)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.browserModeDropdown = QComboBox(NewCrawl)
        self.browserModeDropdown.addItem("")
        self.browserModeDropdown.addItem("")
        self.browserModeDropdown.setObjectName(u"browserModeDropdown")
        sizePolicy.setHeightForWidth(self.browserModeDropdown.sizePolicy().hasHeightForWidth())
        self.browserModeDropdown.setSizePolicy(sizePolicy)
        self.browserModeDropdown.setMinimumSize(QSize(205, 0))

        self.horizontalLayout_3.addWidget(self.browserModeDropdown)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(NewCrawl)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.baseURLText = QLineEdit(NewCrawl)
        self.baseURLText.setObjectName(u"baseURLText")
        self.baseURLText.setMinimumSize(QSize(400, 0))

        self.horizontalLayout_2.addWidget(self.baseURLText)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(NewCrawl)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.ignoreURLsText = QPlainTextEdit(NewCrawl)
        self.ignoreURLsText.setObjectName(u"ignoreURLsText")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ignoreURLsText.sizePolicy().hasHeightForWidth())
        self.ignoreURLsText.setSizePolicy(sizePolicy1)
        self.ignoreURLsText.setMinimumSize(QSize(400, 0))
        self.ignoreURLsText.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout_4.addWidget(self.ignoreURLsText)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.line = QFrame(NewCrawl)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(NewCrawl)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)

        self.maxConcurrencyText = QLineEdit(NewCrawl)
        self.maxConcurrencyText.setObjectName(u"maxConcurrencyText")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.maxConcurrencyText.sizePolicy().hasHeightForWidth())
        self.maxConcurrencyText.setSizePolicy(sizePolicy2)
        self.maxConcurrencyText.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.maxConcurrencyText)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(NewCrawl)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_7.addWidget(self.label_7)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.maxDepthText = QLineEdit(NewCrawl)
        self.maxDepthText.setObjectName(u"maxDepthText")
        sizePolicy2.setHeightForWidth(self.maxDepthText.sizePolicy().hasHeightForWidth())
        self.maxDepthText.setSizePolicy(sizePolicy2)
        self.maxDepthText.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_7.addWidget(self.maxDepthText)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(NewCrawl)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_8.addWidget(self.label_8)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)

        self.xhrTimeoutText = QLineEdit(NewCrawl)
        self.xhrTimeoutText.setObjectName(u"xhrTimeoutText")
        sizePolicy2.setHeightForWidth(self.xhrTimeoutText.sizePolicy().hasHeightForWidth())
        self.xhrTimeoutText.setSizePolicy(sizePolicy2)
        self.xhrTimeoutText.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_8.addWidget(self.xhrTimeoutText)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_9 = QLabel(NewCrawl)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_9.addWidget(self.label_9)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_11)

        self.waitPageText = QLineEdit(NewCrawl)
        self.waitPageText.setObjectName(u"waitPageText")
        sizePolicy2.setHeightForWidth(self.waitPageText.sizePolicy().hasHeightForWidth())
        self.waitPageText.setSizePolicy(sizePolicy2)
        self.waitPageText.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_9.addWidget(self.waitPageText)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_10 = QLabel(NewCrawl)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_10.addWidget(self.label_10)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_12)

        self.logLevelDropdown = QComboBox(NewCrawl)
        self.logLevelDropdown.addItem("")
        self.logLevelDropdown.addItem("")
        self.logLevelDropdown.setObjectName(u"logLevelDropdown")
        sizePolicy.setHeightForWidth(self.logLevelDropdown.sizePolicy().hasHeightForWidth())
        self.logLevelDropdown.setSizePolicy(sizePolicy)
        self.logLevelDropdown.setMinimumSize(QSize(205, 0))

        self.horizontalLayout_10.addWidget(self.logLevelDropdown)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.line_2 = QFrame(NewCrawl)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.cancelButton = QPushButton(NewCrawl)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setAutoDefault(False)

        self.horizontalLayout_5.addWidget(self.cancelButton)

        self.saveButton = QPushButton(NewCrawl)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_5.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(NewCrawl)

        QMetaObject.connectSlotsByName(NewCrawl)
    # setupUi

    def retranslateUi(self, NewCrawl):
        NewCrawl.setWindowTitle(QCoreApplication.translate("NewCrawl", u"New Crawler", None))
        self.label_3.setText(QCoreApplication.translate("NewCrawl", u"Browser:", None))
        self.clientsDropdown.setItemText(0, QCoreApplication.translate("NewCrawl", u"Disabled", None))
        self.clientsDropdown.setItemText(1, QCoreApplication.translate("NewCrawl", u"Only include hosts:", None))
        self.clientsDropdown.setItemText(2, QCoreApplication.translate("NewCrawl", u"Exclude hosts:", None))

        self.label_5.setText(QCoreApplication.translate("NewCrawl", u"Browser mode:", None))
        self.browserModeDropdown.setItemText(0, QCoreApplication.translate("NewCrawl", u"Headless", None))
        self.browserModeDropdown.setItemText(1, QCoreApplication.translate("NewCrawl", u"Normal", None))

        self.label_4.setText(QCoreApplication.translate("NewCrawl", u"Starting URL:", None))
        self.label_2.setText(QCoreApplication.translate("NewCrawl", u"Ignore URLS including (one per line):", None))
        self.label_6.setText(QCoreApplication.translate("NewCrawl", u"Max concurrency:", None))
        self.maxConcurrencyText.setText(QCoreApplication.translate("NewCrawl", u"10", None))
        self.label_7.setText(QCoreApplication.translate("NewCrawl", u"Max depth:", None))
        self.maxDepthText.setText(QCoreApplication.translate("NewCrawl", u"3", None))
        self.label_8.setText(QCoreApplication.translate("NewCrawl", u"XHR timeout (seconds):", None))
        self.xhrTimeoutText.setText(QCoreApplication.translate("NewCrawl", u"5", None))
        self.label_9.setText(QCoreApplication.translate("NewCrawl", u"Wait on each page (seconds):", None))
        self.waitPageText.setText(QCoreApplication.translate("NewCrawl", u"3", None))
        self.label_10.setText(QCoreApplication.translate("NewCrawl", u"Logging level:", None))
        self.logLevelDropdown.setItemText(0, QCoreApplication.translate("NewCrawl", u"Normal", None))
        self.logLevelDropdown.setItemText(1, QCoreApplication.translate("NewCrawl", u"Verbose", None))

        self.cancelButton.setText(QCoreApplication.translate("NewCrawl", u"Cancel", None))
        self.saveButton.setText(QCoreApplication.translate("NewCrawl", u"Start Crawler", None))
    # retranslateUi


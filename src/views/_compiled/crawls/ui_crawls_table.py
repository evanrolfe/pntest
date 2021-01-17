# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crawls_table.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CrawlsTable(object):
    def setupUi(self, CrawlsTable):
        if not CrawlsTable.objectName():
            CrawlsTable.setObjectName(u"CrawlsTable")
        CrawlsTable.resize(424, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CrawlsTable.sizePolicy().hasHeightForWidth())
        CrawlsTable.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(CrawlsTable)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlsTable = QTableView(CrawlsTable)
        self.crawlsTable.setObjectName(u"crawlsTable")

        self.horizontalLayout.addWidget(self.crawlsTable)


        self.retranslateUi(CrawlsTable)

        QMetaObject.connectSlotsByName(CrawlsTable)
    # setupUi

    def retranslateUi(self, CrawlsTable):
        CrawlsTable.setWindowTitle(QCoreApplication.translate("CrawlsTable", u"Form", None))
    # retranslateUi


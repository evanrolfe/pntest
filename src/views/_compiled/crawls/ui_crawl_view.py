# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'crawl_view.ui'
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


class Ui_CrawlView(object):
    def setupUi(self, CrawlView):
        if not CrawlView.objectName():
            CrawlView.setObjectName(u"CrawlView")
        CrawlView.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(CrawlView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlBodyText = QPlainTextEdit(CrawlView)
        self.crawlBodyText.setObjectName(u"crawlBodyText")

        self.horizontalLayout.addWidget(self.crawlBodyText)


        self.retranslateUi(CrawlView)

        QMetaObject.connectSlotsByName(CrawlView)
    # setupUi

    def retranslateUi(self, CrawlView):
        CrawlView.setWindowTitle(QCoreApplication.translate("CrawlView", u"Form", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'requests_page.ui'
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

from widgets.editor.request_group_view import RequestGroupView
from widgets.editor.item_explorer import ItemExplorer


class Ui_RequestsPage(object):
    def setupUi(self, RequestsPage):
        if not RequestsPage.objectName():
            RequestsPage.setObjectName(u"RequestsPage")
        RequestsPage.resize(897, 581)
        self.verticalLayout = QVBoxLayout(RequestsPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(RequestsPage)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.splitter = QSplitter(RequestsPage)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.itemExplorer = ItemExplorer(self.splitter)
        self.itemExplorer.setObjectName(u"itemExplorer")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemExplorer.sizePolicy().hasHeightForWidth())
        self.itemExplorer.setSizePolicy(sizePolicy)
        self.splitter.addWidget(self.itemExplorer)
        self.openRequestTabs = QTabWidget(self.splitter)
        self.openRequestTabs.setObjectName(u"openRequestTabs")
        self.requestGroupView = RequestGroupView()
        self.requestGroupView.setObjectName(u"requestGroupView")
        self.openRequestTabs.addTab(self.requestGroupView, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.openRequestTabs.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.openRequestTabs.addTab(self.tab_3, "")
        self.splitter.addWidget(self.openRequestTabs)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(RequestsPage)

        self.openRequestTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(RequestsPage)
    # setupUi

    def retranslateUi(self, RequestsPage):
        RequestsPage.setWindowTitle(QCoreApplication.translate("RequestsPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("RequestsPage", u"EDITOR", None))
        self.openRequestTabs.setTabText(self.openRequestTabs.indexOf(self.requestGroupView), QCoreApplication.translate("RequestsPage", u"GET /api/posts.json", None))
        self.openRequestTabs.setTabText(self.openRequestTabs.indexOf(self.tab_2), QCoreApplication.translate("RequestsPage", u"POST /login", None))
        self.openRequestTabs.setTabText(self.openRequestTabs.indexOf(self.tab_3), "")
    # retranslateUi


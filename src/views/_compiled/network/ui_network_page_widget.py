# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_page_widget.ui'
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

from widgets.network.network_requests_table import NetworkRequestsTable
from widgets.shared.request_view import RequestView


class Ui_NetworkPageWidget(object):
    def setupUi(self, NetworkPageWidget):
        if not NetworkPageWidget.objectName():
            NetworkPageWidget.setObjectName(u"NetworkPageWidget")
        NetworkPageWidget.resize(897, 581)
        self.verticalLayout = QVBoxLayout(NetworkPageWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.crawlerToolbar = QWidget(NetworkPageWidget)
        self.crawlerToolbar.setObjectName(u"crawlerToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crawlerToolbar.sizePolicy().hasHeightForWidth())
        self.crawlerToolbar.setSizePolicy(sizePolicy)
        self.crawlerToolbar.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.crawlerToolbar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
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

        self.newClientButton = QPushButton(self.crawlerToolbar)
        self.newClientButton.setObjectName(u"newClientButton")
        self.newClientButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.newClientButton)


        self.verticalLayout.addWidget(self.crawlerToolbar)

        self.requestsTableAndViewSplitter = QSplitter(NetworkPageWidget)
        self.requestsTableAndViewSplitter.setObjectName(u"requestsTableAndViewSplitter")
        self.requestsTableAndViewSplitter.setOrientation(Qt.Horizontal)
        self.requestsTableWidget = NetworkRequestsTable(self.requestsTableAndViewSplitter)
        self.requestsTableWidget.setObjectName(u"requestsTableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.requestsTableWidget.sizePolicy().hasHeightForWidth())
        self.requestsTableWidget.setSizePolicy(sizePolicy1)
        self.requestsTableWidget.setMinimumSize(QSize(740, 0))
        self.requestsTableAndViewSplitter.addWidget(self.requestsTableWidget)
        self.requestViewWidget = RequestView(self.requestsTableAndViewSplitter)
        self.requestViewWidget.setObjectName(u"requestViewWidget")
        sizePolicy1.setHeightForWidth(self.requestViewWidget.sizePolicy().hasHeightForWidth())
        self.requestViewWidget.setSizePolicy(sizePolicy1)
        self.requestsTableAndViewSplitter.addWidget(self.requestViewWidget)

        self.verticalLayout.addWidget(self.requestsTableAndViewSplitter)


        self.retranslateUi(NetworkPageWidget)

        QMetaObject.connectSlotsByName(NetworkPageWidget)
    # setupUi

    def retranslateUi(self, NetworkPageWidget):
        NetworkPageWidget.setWindowTitle(QCoreApplication.translate("NetworkPageWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("NetworkPageWidget", u"NETWORK", None))
        self.newClientButton.setText(QCoreApplication.translate("NetworkPageWidget", u"HTTP", None))
    # retranslateUi


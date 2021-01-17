# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'network_display_filters.ui'
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


class Ui_NetworkDisplayFilters(object):
    def setupUi(self, NetworkDisplayFilters):
        if not NetworkDisplayFilters.objectName():
            NetworkDisplayFilters.setObjectName(u"NetworkDisplayFilters")
        NetworkDisplayFilters.resize(700, 300)
        self.verticalLayout_2 = QVBoxLayout(NetworkDisplayFilters)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descLabel = QLabel(NetworkDisplayFilters)
        self.descLabel.setObjectName(u"descLabel")

        self.verticalLayout.addWidget(self.descLabel)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(NetworkDisplayFilters)

        QMetaObject.connectSlotsByName(NetworkDisplayFilters)
    # setupUi

    def retranslateUi(self, NetworkDisplayFilters):
        NetworkDisplayFilters.setWindowTitle(QCoreApplication.translate("NetworkDisplayFilters", u"New Client", None))
        self.descLabel.setText(QCoreApplication.translate("NetworkDisplayFilters", u"DISPLAY FILTERS GO HERE!", None))
    # retranslateUi


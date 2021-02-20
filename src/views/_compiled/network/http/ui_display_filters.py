# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'display_filters.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DisplayFilters(object):
    def setupUi(self, DisplayFilters):
        if not DisplayFilters.objectName():
            DisplayFilters.setObjectName(u"DisplayFilters")
        DisplayFilters.resize(700, 300)
        self.verticalLayout_2 = QVBoxLayout(DisplayFilters)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descLabel = QLabel(DisplayFilters)
        self.descLabel.setObjectName(u"descLabel")

        self.verticalLayout.addWidget(self.descLabel)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(DisplayFilters)

        QMetaObject.connectSlotsByName(DisplayFilters)
    # setupUi

    def retranslateUi(self, DisplayFilters):
        DisplayFilters.setWindowTitle(QCoreApplication.translate("DisplayFilters", u"New Client", None))
        self.descLabel.setText(QCoreApplication.translate("DisplayFilters", u"DISPLAY FILTERS GO HERE!", None))
    # retranslateUi


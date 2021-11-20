# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'examples_table.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ExamplesTable(object):
    def setupUi(self, ExamplesTable):
        if not ExamplesTable.objectName():
            ExamplesTable.setObjectName(u"ExamplesTable")
        ExamplesTable.resize(424, 702)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExamplesTable.sizePolicy().hasHeightForWidth())
        ExamplesTable.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(ExamplesTable)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(ExamplesTable)
        self.label.setObjectName(u"label")
        self.label.setMargin(10)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.table = QTableView(ExamplesTable)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(ExamplesTable)

        QMetaObject.connectSlotsByName(ExamplesTable)
    # setupUi

    def retranslateUi(self, ExamplesTable):
        ExamplesTable.setWindowTitle(QCoreApplication.translate("ExamplesTable", u"Form", None))
        self.label.setText(QCoreApplication.translate("ExamplesTable", u"Saved Examples", None))
    # retranslateUi


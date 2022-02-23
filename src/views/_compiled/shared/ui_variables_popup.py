# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'variables_popup.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_VariablesPopup(object):
    def setupUi(self, VariablesPopup):
        if not VariablesPopup.objectName():
            VariablesPopup.setObjectName(u"VariablesPopup")
        VariablesPopup.resize(485, 313)
        self.verticalLayout = QVBoxLayout(VariablesPopup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(VariablesPopup)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.varsTable = QWidget(VariablesPopup)
        self.varsTable.setObjectName(u"varsTable")

        self.verticalLayout.addWidget(self.varsTable)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.cancelButton = QPushButton(VariablesPopup)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setAutoDefault(False)

        self.horizontalLayout_5.addWidget(self.cancelButton)

        self.saveButton = QPushButton(VariablesPopup)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_5.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(VariablesPopup)

        QMetaObject.connectSlotsByName(VariablesPopup)
    # setupUi

    def retranslateUi(self, VariablesPopup):
        VariablesPopup.setWindowTitle(QCoreApplication.translate("VariablesPopup", u"Global Variables", None))
        self.label.setText(QCoreApplication.translate("VariablesPopup", u"Global Variables are available in all requests and in the interceptor.", None))
        self.cancelButton.setText(QCoreApplication.translate("VariablesPopup", u"Cancel", None))
        self.saveButton.setText(QCoreApplication.translate("VariablesPopup", u"Save", None))
    # retranslateUi


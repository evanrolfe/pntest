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
        DisplayFilters.resize(485, 313)
        self.verticalLayout = QVBoxLayout(DisplayFilters)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_3 = QLabel(DisplayFilters)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.hostSettingDropdown = QComboBox(DisplayFilters)
        self.hostSettingDropdown.addItem("")
        self.hostSettingDropdown.addItem("")
        self.hostSettingDropdown.addItem("")
        self.hostSettingDropdown.setObjectName(u"hostSettingDropdown")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hostSettingDropdown.sizePolicy().hasHeightForWidth())
        self.hostSettingDropdown.setSizePolicy(sizePolicy)
        self.hostSettingDropdown.setMinimumSize(QSize(205, 0))

        self.horizontalLayout.addWidget(self.hostSettingDropdown)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(DisplayFilters)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.hostsText = QPlainTextEdit(DisplayFilters)
        self.hostsText.setObjectName(u"hostsText")

        self.horizontalLayout_2.addWidget(self.hostsText)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_4 = QLabel(DisplayFilters)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.pathSettingDropdown = QComboBox(DisplayFilters)
        self.pathSettingDropdown.addItem("")
        self.pathSettingDropdown.addItem("")
        self.pathSettingDropdown.addItem("")
        self.pathSettingDropdown.setObjectName(u"pathSettingDropdown")
        sizePolicy.setHeightForWidth(self.pathSettingDropdown.sizePolicy().hasHeightForWidth())
        self.pathSettingDropdown.setSizePolicy(sizePolicy)
        self.pathSettingDropdown.setMinimumSize(QSize(205, 0))

        self.horizontalLayout_3.addWidget(self.pathSettingDropdown)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(DisplayFilters)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.pathsText = QPlainTextEdit(DisplayFilters)
        self.pathsText.setObjectName(u"pathsText")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pathsText.sizePolicy().hasHeightForWidth())
        self.pathsText.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.pathsText)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_2 = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.cancelButton = QPushButton(DisplayFilters)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setAutoDefault(False)

        self.horizontalLayout_5.addWidget(self.cancelButton)

        self.saveButton = QPushButton(DisplayFilters)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_5.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(DisplayFilters)

        QMetaObject.connectSlotsByName(DisplayFilters)
    # setupUi

    def retranslateUi(self, DisplayFilters):
        DisplayFilters.setWindowTitle(QCoreApplication.translate("DisplayFilters", u"Edit Display Filters", None))
        self.label_3.setText(QCoreApplication.translate("DisplayFilters", u"Host Filter:", None))
        self.hostSettingDropdown.setItemText(0, QCoreApplication.translate("DisplayFilters", u"Disabled", None))
        self.hostSettingDropdown.setItemText(1, QCoreApplication.translate("DisplayFilters", u"Only include hosts:", None))
        self.hostSettingDropdown.setItemText(2, QCoreApplication.translate("DisplayFilters", u"Exclude hosts:", None))

        self.label.setText(QCoreApplication.translate("DisplayFilters", u"Hosts (one per line):", None))
        self.label_4.setText(QCoreApplication.translate("DisplayFilters", u"Path Filter:", None))
        self.pathSettingDropdown.setItemText(0, QCoreApplication.translate("DisplayFilters", u"Disabled", None))
        self.pathSettingDropdown.setItemText(1, QCoreApplication.translate("DisplayFilters", u"Only include paths containing:", None))
        self.pathSettingDropdown.setItemText(2, QCoreApplication.translate("DisplayFilters", u"Exclude paths containing:", None))

        self.label_2.setText(QCoreApplication.translate("DisplayFilters", u"Paths (one per line):", None))
        self.cancelButton.setText(QCoreApplication.translate("DisplayFilters", u"Cancel", None))
        self.saveButton.setText(QCoreApplication.translate("DisplayFilters", u"Save", None))
    # retranslateUi


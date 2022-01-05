# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor_page.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from widgets.editor.tabs import Tabs
from widgets.editor.item_explorer import ItemExplorer


class Ui_EditorPage(object):
    def setupUi(self, EditorPage):
        if not EditorPage.objectName():
            EditorPage.setObjectName(u"EditorPage")
        EditorPage.resize(897, 581)
        self.verticalLayout = QVBoxLayout(EditorPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pageToolbar = QWidget(EditorPage)
        self.pageToolbar.setObjectName(u"pageToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.pageToolbar)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.pageToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.pageToolbar)

        self.editorSplitter = QSplitter(EditorPage)
        self.editorSplitter.setObjectName(u"editorSplitter")
        self.editorSplitter.setOrientation(Qt.Horizontal)
        self.itemExplorer = ItemExplorer(self.editorSplitter)
        self.itemExplorer.setObjectName(u"itemExplorer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.itemExplorer.sizePolicy().hasHeightForWidth())
        self.itemExplorer.setSizePolicy(sizePolicy1)
        self.editorSplitter.addWidget(self.itemExplorer)
        self.editorTabs = Tabs(self.editorSplitter)
        self.editorTabs.setObjectName(u"editorTabs")
        self.editorSplitter.addWidget(self.editorTabs)

        self.verticalLayout.addWidget(self.editorSplitter)


        self.retranslateUi(EditorPage)

        QMetaObject.connectSlotsByName(EditorPage)
    # setupUi

    def retranslateUi(self, EditorPage):
        EditorPage.setWindowTitle(QCoreApplication.translate("EditorPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("EditorPage", u"EDITOR", None))
    # retranslateUi


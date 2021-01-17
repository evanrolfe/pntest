# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editor_page.ui'
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
        self.crawlerToolbar = QWidget(EditorPage)
        self.crawlerToolbar.setObjectName(u"crawlerToolbar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.crawlerToolbar.sizePolicy().hasHeightForWidth())
        self.crawlerToolbar.setSizePolicy(sizePolicy)
        self.crawlerToolbar.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.crawlerToolbar)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 5, 10, 5)
        self.label = QLabel(self.crawlerToolbar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(158, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.crawlerToolbar)

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
        self.tabs = Tabs(self.editorSplitter)
        self.tabs.setObjectName(u"tabs")
        self.editorSplitter.addWidget(self.tabs)

        self.verticalLayout.addWidget(self.editorSplitter)


        self.retranslateUi(EditorPage)

        QMetaObject.connectSlotsByName(EditorPage)
    # setupUi

    def retranslateUi(self, EditorPage):
        EditorPage.setWindowTitle(QCoreApplication.translate("EditorPage", u"Form", None))
        self.label.setText(QCoreApplication.translate("EditorPage", u"EDITOR", None))
    # retranslateUi


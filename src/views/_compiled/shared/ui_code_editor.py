# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'code_editor.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView


class Ui_CodeEditor(object):
    def setupUi(self, CodeEditor):
        if not CodeEditor.objectName():
            CodeEditor.setObjectName(u"CodeEditor")
        CodeEditor.resize(880, 521)
        self.verticalLayout = QVBoxLayout(CodeEditor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.code = QWebEngineView(CodeEditor)
        self.code.setObjectName(u"code")

        self.verticalLayout.addWidget(self.code)


        self.retranslateUi(CodeEditor)

        QMetaObject.connectSlotsByName(CodeEditor)
    # setupUi

    def retranslateUi(self, CodeEditor):
        pass
    # retranslateUi


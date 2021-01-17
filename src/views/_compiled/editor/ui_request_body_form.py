# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'request_body_form.ui'
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


class Ui_RequestBodyForm(object):
    def setupUi(self, RequestBodyForm):
        if not RequestBodyForm.objectName():
            RequestBodyForm.setObjectName(u"RequestBodyForm")
        RequestBodyForm.resize(880, 521)
        self.verticalLayout = QVBoxLayout(RequestBodyForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.requestBodyInput = QPlainTextEdit(RequestBodyForm)
        self.requestBodyInput.setObjectName(u"requestBodyInput")

        self.verticalLayout.addWidget(self.requestBodyInput)


        self.retranslateUi(RequestBodyForm)

        QMetaObject.connectSlotsByName(RequestBodyForm)
    # setupUi

    def retranslateUi(self, RequestBodyForm):
        pass
    # retranslateUi


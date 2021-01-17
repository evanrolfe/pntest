# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_client_modal.ui'
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


class Ui_NewClientModal(object):
    def setupUi(self, NewClientModal):
        if not NewClientModal.objectName():
            NewClientModal.setObjectName(u"NewClientModal")
        NewClientModal.resize(700, 300)
        self.verticalLayout_2 = QVBoxLayout(NewClientModal)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.chromiumButton = QPushButton(NewClientModal)
        self.chromiumButton.setObjectName(u"chromiumButton")

        self.horizontalLayout.addWidget(self.chromiumButton)

        self.chromeButton = QPushButton(NewClientModal)
        self.chromeButton.setObjectName(u"chromeButton")

        self.horizontalLayout.addWidget(self.chromeButton)

        self.firefoxButton = QPushButton(NewClientModal)
        self.firefoxButton.setObjectName(u"firefoxButton")

        self.horizontalLayout.addWidget(self.firefoxButton)

        self.anythingButton = QPushButton(NewClientModal)
        self.anythingButton.setObjectName(u"anythingButton")

        self.horizontalLayout.addWidget(self.anythingButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.descLabel = QLabel(NewClientModal)
        self.descLabel.setObjectName(u"descLabel")

        self.verticalLayout.addWidget(self.descLabel)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.line_2 = QFrame(NewClientModal)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(388, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.cancelButton = QPushButton(NewClientModal)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_2.addWidget(self.cancelButton)

        self.launchButton = QPushButton(NewClientModal)
        self.launchButton.setObjectName(u"launchButton")

        self.horizontalLayout_2.addWidget(self.launchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.retranslateUi(NewClientModal)

        QMetaObject.connectSlotsByName(NewClientModal)
    # setupUi

    def retranslateUi(self, NewClientModal):
        NewClientModal.setWindowTitle(QCoreApplication.translate("NewClientModal", u"New Client", None))
        self.chromiumButton.setText(QCoreApplication.translate("NewClientModal", u"Chromium", None))
        self.chromeButton.setText(QCoreApplication.translate("NewClientModal", u"Chrome", None))
        self.firefoxButton.setText(QCoreApplication.translate("NewClientModal", u"Firefox", None))
        self.anythingButton.setText(QCoreApplication.translate("NewClientModal", u"Anything (Port 8082)", None))
        self.descLabel.setText(QCoreApplication.translate("NewClientModal", u"Launch a new Chromium instance:", None))
        self.cancelButton.setText(QCoreApplication.translate("NewClientModal", u"Cancel", None))
        self.launchButton.setText(QCoreApplication.translate("NewClientModal", u"Launch", None))
    # retranslateUi


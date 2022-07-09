# Form implementation generated from reading ui file 'src/views/clients/clients_page.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ClientsPage(object):
    def setupUi(self, ClientsPage):
        ClientsPage.setObjectName("ClientsPage")
        ClientsPage.resize(897, 581)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ClientsPage)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pageToolbar = QtWidgets.QWidget(ClientsPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pageToolbar.setObjectName("pageToolbar")
        self.headerLayout = QtWidgets.QHBoxLayout(self.pageToolbar)
        self.headerLayout.setContentsMargins(10, 5, 10, 5)
        self.headerLayout.setObjectName("headerLayout")
        self.label = QtWidgets.QLabel(self.pageToolbar)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.headerLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(158, 40, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.headerLayout.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.pageToolbar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(ClientsPage)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_4 = QtWidgets.QLabel(ClientsPage)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.clientsTable = ClientsTable(ClientsPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clientsTable.sizePolicy().hasHeightForWidth())
        self.clientsTable.setSizePolicy(sizePolicy)
        self.clientsTable.setMinimumSize(QtCore.QSize(0, 200))
        self.clientsTable.setMaximumSize(QtCore.QSize(16777215, 99999))
        self.clientsTable.setObjectName("clientsTable")
        self.verticalLayout.addWidget(self.clientsTable)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName("gridLayout")
        self.chromeButton = QtWidgets.QPushButton(ClientsPage)
        self.chromeButton.setEnabled(False)
        self.chromeButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.chromeButton.setObjectName("chromeButton")
        self.gridLayout.addWidget(self.chromeButton, 0, 0, 1, 1)
        self.chromiumButton = QtWidgets.QPushButton(ClientsPage)
        self.chromiumButton.setEnabled(False)
        self.chromiumButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.chromiumButton.setObjectName("chromiumButton")
        self.gridLayout.addWidget(self.chromiumButton, 0, 1, 1, 1)
        self.firefoxButton = QtWidgets.QPushButton(ClientsPage)
        self.firefoxButton.setEnabled(False)
        self.firefoxButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.firefoxButton.setObjectName("firefoxButton")
        self.gridLayout.addWidget(self.firefoxButton, 0, 2, 1, 1)
        self.terminalButton = QtWidgets.QPushButton(ClientsPage)
        self.terminalButton.setEnabled(False)
        self.terminalButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.terminalButton.setObjectName("terminalButton")
        self.gridLayout.addWidget(self.terminalButton, 0, 3, 1, 1)
        self.existingTerminalButton = QtWidgets.QPushButton(ClientsPage)
        self.existingTerminalButton.setEnabled(False)
        self.existingTerminalButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.existingTerminalButton.setObjectName("existingTerminalButton")
        self.gridLayout.addWidget(self.existingTerminalButton, 0, 4, 1, 1)
        self.anythingButton = QtWidgets.QPushButton(ClientsPage)
        self.anythingButton.setEnabled(False)
        self.anythingButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.anythingButton.setObjectName("anythingButton")
        self.gridLayout.addWidget(self.anythingButton, 1, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 217, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)

        self.retranslateUi(ClientsPage)
        QtCore.QMetaObject.connectSlotsByName(ClientsPage)

    def retranslateUi(self, ClientsPage):
        _translate = QtCore.QCoreApplication.translate
        ClientsPage.setWindowTitle(_translate("ClientsPage", "Form"))
        self.label.setText(_translate("ClientsPage", "CLIENTS"))
        self.label_2.setText(_translate("ClientsPage", "Launch a Client"))
        self.label_4.setText(_translate("ClientsPage", "To view and intercept HTTP(S) traffic, you need to launch a pre-configured and isolated client like a browser or a terminal session.\n"
"\n"
"Click an option below to start."))
        self.chromeButton.setText(_translate("ClientsPage", "Chrome"))
        self.chromiumButton.setText(_translate("ClientsPage", "Chromium"))
        self.firefoxButton.setText(_translate("ClientsPage", "Firefox"))
        self.terminalButton.setText(_translate("ClientsPage", "Terminal"))
        self.existingTerminalButton.setText(_translate("ClientsPage", "Existing Terminal"))
        self.anythingButton.setText(_translate("ClientsPage", "Anything"))
from widgets.clients.clients_table import ClientsTable

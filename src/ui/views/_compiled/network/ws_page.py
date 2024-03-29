# Form implementation generated from reading ui file 'src/ui/views/network/ws_page.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WsPage(object):
    def setupUi(self, WsPage):
        WsPage.setObjectName("WsPage")
        WsPage.resize(1400, 700)
        self.verticalLayout = QtWidgets.QVBoxLayout(WsPage)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pageToolbar = QtWidgets.QWidget(WsPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pageToolbar.setObjectName("pageToolbar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.pageToolbar)
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.pageToolbar)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.toggleButton = QtWidgets.QPushButton(self.pageToolbar)
        self.toggleButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.toggleButton.setObjectName("toggleButton")
        self.horizontalLayout.addWidget(self.toggleButton)
        self.verticalLayout.addWidget(self.pageToolbar)
        self.messagesTableAndViewSplitter = QtWidgets.QSplitter(WsPage)
        self.messagesTableAndViewSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.messagesTableAndViewSplitter.setObjectName("messagesTableAndViewSplitter")
        self.messagesTable = MessagesTable(self.messagesTableAndViewSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messagesTable.sizePolicy().hasHeightForWidth())
        self.messagesTable.setSizePolicy(sizePolicy)
        self.messagesTable.setMinimumSize(QtCore.QSize(740, 0))
        self.messagesTable.setObjectName("messagesTable")
        self.messageViewWidget = MessageView(self.messagesTableAndViewSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageViewWidget.sizePolicy().hasHeightForWidth())
        self.messageViewWidget.setSizePolicy(sizePolicy)
        self.messageViewWidget.setObjectName("messageViewWidget")
        self.verticalLayout.addWidget(self.messagesTableAndViewSplitter)

        self.retranslateUi(WsPage)
        QtCore.QMetaObject.connectSlotsByName(WsPage)

    def retranslateUi(self, WsPage):
        _translate = QtCore.QCoreApplication.translate
        WsPage.setWindowTitle(_translate("WsPage", "Form"))
        self.label.setText(_translate("WsPage", "NETWORK - WEBSOCKETS"))
        self.toggleButton.setText(_translate("WsPage", "HTTP"))
from ui.widgets.network.ws.message_view import MessageView
from ui.widgets.network.ws.messages_table import MessagesTable

# Form implementation generated from reading ui file 'src/views/network/ws/messages_table.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MessagesTable(object):
    def setupUi(self, MessagesTable):
        MessagesTable.setObjectName("MessagesTable")
        MessagesTable.resize(509, 702)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MessagesTable.sizePolicy().hasHeightForWidth())
        MessagesTable.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(MessagesTable)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.searchBox = QtWidgets.QLineEdit(MessagesTable)
        self.searchBox.setObjectName("searchBox")
        self.verticalLayout_2.addWidget(self.searchBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.displayFiltersButton = QtWidgets.QPushButton(MessagesTable)
        self.displayFiltersButton.setObjectName("displayFiltersButton")
        self.horizontalLayout.addWidget(self.displayFiltersButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.messagesTable = HoverableQTableView(MessagesTable)
        self.messagesTable.setObjectName("messagesTable")
        self.verticalLayout_3.addWidget(self.messagesTable)

        self.retranslateUi(MessagesTable)
        QtCore.QMetaObject.connectSlotsByName(MessagesTable)

    def retranslateUi(self, MessagesTable):
        _translate = QtCore.QCoreApplication.translate
        MessagesTable.setWindowTitle(_translate("MessagesTable", "Form"))
        self.searchBox.setPlaceholderText(_translate("MessagesTable", "Search"))
        self.displayFiltersButton.setText(_translate("MessagesTable", "Display"))
from widgets.qt.hoverable_q_table_view import HoverableQTableView

# Form implementation generated from reading ui file 'src/ui/views/clients/clients_table.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ClientsTable(object):
    def setupUi(self, ClientsTable):
        ClientsTable.setObjectName("ClientsTable")
        ClientsTable.resize(424, 702)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ClientsTable.sizePolicy().hasHeightForWidth())
        ClientsTable.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ClientsTable)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.clientsTable = QtWidgets.QTableView(ClientsTable)
        self.clientsTable.setObjectName("clientsTable")
        self.horizontalLayout.addWidget(self.clientsTable)

        self.retranslateUi(ClientsTable)
        QtCore.QMetaObject.connectSlotsByName(ClientsTable)

    def retranslateUi(self, ClientsTable):
        _translate = QtCore.QCoreApplication.translate
        ClientsTable.setWindowTitle(_translate("ClientsTable", "Form"))

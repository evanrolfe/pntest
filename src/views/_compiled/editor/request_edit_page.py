# Form implementation generated from reading ui file 'src/views/editor/request_edit_page.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RequestEditPage(object):
    def setupUi(self, RequestEditPage):
        RequestEditPage.setObjectName("RequestEditPage")
        RequestEditPage.resize(897, 581)
        self.horizontalLayout = QtWidgets.QHBoxLayout(RequestEditPage)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.requestEditSplitter = QtWidgets.QSplitter(RequestEditPage)
        self.requestEditSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.requestEditSplitter.setObjectName("requestEditSplitter")
        self.examplesTable = ExamplesTable(self.requestEditSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.examplesTable.sizePolicy().hasHeightForWidth())
        self.examplesTable.setSizePolicy(sizePolicy)
        self.examplesTable.setMinimumSize(QtCore.QSize(0, 200))
        self.examplesTable.setMaximumSize(QtCore.QSize(16777215, 99999))
        self.examplesTable.setObjectName("examplesTable")
        self.layoutWidget = QtWidgets.QWidget(self.requestEditSplitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout1 = QtWidgets.QHBoxLayout()
        self.layout1.setContentsMargins(10, 10, 10, -1)
        self.layout1.setObjectName("layout1")
        self.toggleExamplesButton = QtWidgets.QPushButton(self.layoutWidget)
        self.toggleExamplesButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.toggleExamplesButton.setObjectName("toggleExamplesButton")
        self.layout1.addWidget(self.toggleExamplesButton)
        spacerItem = QtWidgets.QSpacerItem(388, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.layout1.addItem(spacerItem)
        self.verticalLayout.addLayout(self.layout1)
        self.requestActionsLayout = QtWidgets.QHBoxLayout()
        self.requestActionsLayout.setContentsMargins(10, 10, 10, 10)
        self.requestActionsLayout.setObjectName("requestActionsLayout")
        self.methodInput = QtWidgets.QComboBox(self.layoutWidget)
        self.methodInput.setObjectName("methodInput")
        self.requestActionsLayout.addWidget(self.methodInput)
        self.urlInput = LineScintilla(self.layoutWidget)
        self.urlInput.setMinimumSize(QtCore.QSize(300, 32))
        self.urlInput.setMaximumSize(QtCore.QSize(9999, 32))
        self.urlInput.setObjectName("urlInput")
        self.requestActionsLayout.addWidget(self.urlInput)
        self.sendButton = QtWidgets.QPushButton(self.layoutWidget)
        self.sendButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sendButton.setObjectName("sendButton")
        self.requestActionsLayout.addWidget(self.sendButton)
        self.saveButton = QtWidgets.QPushButton(self.layoutWidget)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.saveButton.setObjectName("saveButton")
        self.requestActionsLayout.addWidget(self.saveButton)
        self.actionsButton = QtWidgets.QPushButton(self.layoutWidget)
        self.actionsButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.actionsButton.setObjectName("actionsButton")
        self.requestActionsLayout.addWidget(self.actionsButton)
        self.verticalLayout.addLayout(self.requestActionsLayout)
        self.layout2 = QtWidgets.QHBoxLayout()
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout2.setObjectName("layout2")
        self.flowView = FlowView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.flowView.sizePolicy().hasHeightForWidth())
        self.flowView.setSizePolicy(sizePolicy)
        self.flowView.setObjectName("flowView")
        self.layout2.addWidget(self.flowView)
        self.verticalLayout.addLayout(self.layout2)
        self.horizontalLayout.addWidget(self.requestEditSplitter)

        self.retranslateUi(RequestEditPage)
        QtCore.QMetaObject.connectSlotsByName(RequestEditPage)

    def retranslateUi(self, RequestEditPage):
        _translate = QtCore.QCoreApplication.translate
        RequestEditPage.setWindowTitle(_translate("RequestEditPage", "Form"))
        self.toggleExamplesButton.setText(_translate("RequestEditPage", "Saved Examples (10) <<"))
        self.sendButton.setText(_translate("RequestEditPage", "Send"))
        self.saveButton.setText(_translate("RequestEditPage", "Save"))
        self.actionsButton.setText(_translate("RequestEditPage", "..."))
from widgets.editor.examples_table import ExamplesTable
from widgets.shared.flow_view import FlowView
from widgets.shared.line_scintilla import LineScintilla

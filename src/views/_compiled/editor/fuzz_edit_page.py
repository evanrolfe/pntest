# Form implementation generated from reading ui file 'src/views/editor/fuzz_edit_page.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FuzzEditPage(object):
    def setupUi(self, FuzzEditPage):
        FuzzEditPage.setObjectName("FuzzEditPage")
        FuzzEditPage.resize(897, 581)
        self.horizontalLayout = QtWidgets.QHBoxLayout(FuzzEditPage)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fuzzEditSplitter = QtWidgets.QSplitter(FuzzEditPage)
        self.fuzzEditSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.fuzzEditSplitter.setObjectName("fuzzEditSplitter")
        self.examplesTable = ExamplesTable(self.fuzzEditSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.examplesTable.sizePolicy().hasHeightForWidth())
        self.examplesTable.setSizePolicy(sizePolicy)
        self.examplesTable.setMinimumSize(QtCore.QSize(0, 200))
        self.examplesTable.setMaximumSize(QtCore.QSize(16777215, 99999))
        self.examplesTable.setObjectName("examplesTable")
        self.layoutWidget = QtWidgets.QWidget(self.fuzzEditSplitter)
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
        self.requestActionsLayout.setContentsMargins(10, 10, 10, 20)
        self.requestActionsLayout.setObjectName("requestActionsLayout")
        self.methodInput = QtWidgets.QComboBox(self.layoutWidget)
        self.methodInput.setObjectName("methodInput")
        self.requestActionsLayout.addWidget(self.methodInput)
        self.urlInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.urlInput.setMinimumSize(QtCore.QSize(300, 0))
        self.urlInput.setObjectName("urlInput")
        self.requestActionsLayout.addWidget(self.urlInput)
        self.fuzzButton = QtWidgets.QPushButton(self.layoutWidget)
        self.fuzzButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.fuzzButton.setObjectName("fuzzButton")
        self.requestActionsLayout.addWidget(self.fuzzButton)
        self.saveButton = QtWidgets.QPushButton(self.layoutWidget)
        self.saveButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.saveButton.setObjectName("saveButton")
        self.requestActionsLayout.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.requestActionsLayout)
        self.layout2 = QtWidgets.QHBoxLayout()
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout2.setObjectName("layout2")
        self.fuzzView = FuzzView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fuzzView.sizePolicy().hasHeightForWidth())
        self.fuzzView.setSizePolicy(sizePolicy)
        self.fuzzView.setObjectName("fuzzView")
        self.layout2.addWidget(self.fuzzView)
        self.verticalLayout.addLayout(self.layout2)
        self.horizontalLayout.addWidget(self.fuzzEditSplitter)

        self.retranslateUi(FuzzEditPage)
        QtCore.QMetaObject.connectSlotsByName(FuzzEditPage)

    def retranslateUi(self, FuzzEditPage):
        _translate = QtCore.QCoreApplication.translate
        FuzzEditPage.setWindowTitle(_translate("FuzzEditPage", "Form"))
        self.toggleExamplesButton.setText(_translate("FuzzEditPage", "Saved Examples (10) <<"))
        self.fuzzButton.setText(_translate("FuzzEditPage", "Fuzz"))
        self.saveButton.setText(_translate("FuzzEditPage", "Save"))
from widgets.editor.examples_table import ExamplesTable
from widgets.editor.fuzz_view import FuzzView

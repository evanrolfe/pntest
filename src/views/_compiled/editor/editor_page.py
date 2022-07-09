# Form implementation generated from reading ui file 'src/views/editor/editor_page.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditorPage(object):
    def setupUi(self, EditorPage):
        EditorPage.setObjectName("EditorPage")
        EditorPage.resize(897, 581)
        self.verticalLayout = QtWidgets.QVBoxLayout(EditorPage)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pageToolbar = QtWidgets.QWidget(EditorPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageToolbar.sizePolicy().hasHeightForWidth())
        self.pageToolbar.setSizePolicy(sizePolicy)
        self.pageToolbar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pageToolbar.setObjectName("pageToolbar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.pageToolbar)
        self.horizontalLayout_2.setContentsMargins(10, 5, 10, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.pageToolbar)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(158, 20, QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.varsButton = QtWidgets.QPushButton(self.pageToolbar)
        self.varsButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.varsButton.setObjectName("varsButton")
        self.horizontalLayout_2.addWidget(self.varsButton)
        self.verticalLayout.addWidget(self.pageToolbar)
        self.editorSplitter = QtWidgets.QSplitter(EditorPage)
        self.editorSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.editorSplitter.setObjectName("editorSplitter")
        self.itemExplorer = ItemExplorer(self.editorSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.itemExplorer.sizePolicy().hasHeightForWidth())
        self.itemExplorer.setSizePolicy(sizePolicy)
        self.itemExplorer.setObjectName("itemExplorer")
        self.editorTabs = Tabs(self.editorSplitter)
        self.editorTabs.setObjectName("editorTabs")
        self.verticalLayout.addWidget(self.editorSplitter)

        self.retranslateUi(EditorPage)
        QtCore.QMetaObject.connectSlotsByName(EditorPage)

    def retranslateUi(self, EditorPage):
        _translate = QtCore.QCoreApplication.translate
        EditorPage.setWindowTitle(_translate("EditorPage", "Form"))
        self.label.setText(_translate("EditorPage", "EDITOR"))
        self.varsButton.setText(_translate("EditorPage", "Variables"))
from widgets.editor.item_explorer import ItemExplorer
from widgets.editor.tabs import Tabs

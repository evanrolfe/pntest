# Form implementation generated from reading ui file 'src/views/shared/encoders_popup.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EncodersPopup(object):
    def setupUi(self, EncodersPopup):
        EncodersPopup.setObjectName("EncodersPopup")
        EncodersPopup.resize(600, 330)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EncodersPopup.sizePolicy().hasHeightForWidth())
        EncodersPopup.setSizePolicy(sizePolicy)
        EncodersPopup.setMaximumSize(QtCore.QSize(16777215, 330))
        EncodersPopup.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EncodersPopup)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.vertLayout = QtWidgets.QVBoxLayout()
        self.vertLayout.setSpacing(5)
        self.vertLayout.setObjectName("vertLayout")
        self.inputText = QtWidgets.QPlainTextEdit(EncodersPopup)
        self.inputText.setMaximumSize(QtCore.QSize(16777215, 40))
        self.inputText.setObjectName("inputText")
        self.vertLayout.addWidget(self.inputText)
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.vertLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.vertLayout)
        self.tabWidget = QtWidgets.QTabWidget(EncodersPopup)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.encodersLayout = QtWidgets.QVBoxLayout(self.tab)
        self.encodersLayout.setContentsMargins(0, 10, 0, 0)
        self.encodersLayout.setObjectName("encodersLayout")
        self.tabWidget.addTab(self.tab, "")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.decodersLayout = QtWidgets.QVBoxLayout(self.tab1)
        self.decodersLayout.setContentsMargins(0, 10, 0, 0)
        self.decodersLayout.setObjectName("decodersLayout")
        self.tabWidget.addTab(self.tab1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.cancelButton = QtWidgets.QPushButton(EncodersPopup)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.saveButton = QtWidgets.QPushButton(EncodersPopup)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_5.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(EncodersPopup)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(EncodersPopup)

    def retranslateUi(self, EncodersPopup):
        _translate = QtCore.QCoreApplication.translate
        EncodersPopup.setWindowTitle(_translate("EncodersPopup", "Try all encoders"))
        self.inputText.setPlaceholderText(_translate("EncodersPopup", "Enter text to encode"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("EncodersPopup", "Encode"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("EncodersPopup", "Decode"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("EncodersPopup", "Hash"))
        self.cancelButton.setText(_translate("EncodersPopup", "Cancel"))
        self.saveButton.setText(_translate("EncodersPopup", "Apply"))

# Form implementation generated from reading ui file 'src/views/preferences_window.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PreferencesWindow(object):
    def setupUi(self, PreferencesWindow):
        PreferencesWindow.setObjectName("PreferencesWindow")
        PreferencesWindow.resize(738, 336)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PreferencesWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(PreferencesWindow)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.layoutWidget = QtWidgets.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 716, 237))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.proxyPortsInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.proxyPortsInput.setMinimumSize(QtCore.QSize(400, 0))
        self.proxyPortsInput.setObjectName("proxyPortsInput")
        self.horizontalLayout_6.addWidget(self.proxyPortsInput)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.chromeAuto = QtWidgets.QRadioButton(self.layoutWidget)
        self.chromeAuto.setObjectName("chromeAuto")
        self.buttonGroup = QtWidgets.QButtonGroup(PreferencesWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.chromeAuto)
        self.horizontalLayout_7.addWidget(self.chromeAuto)
        self.chromeCustom = QtWidgets.QRadioButton(self.layoutWidget)
        self.chromeCustom.setObjectName("chromeCustom")
        self.buttonGroup.addButton(self.chromeCustom)
        self.horizontalLayout_7.addWidget(self.chromeCustom)
        self.chromeCommandInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.chromeCommandInput.setMinimumSize(QtCore.QSize(400, 0))
        self.chromeCommandInput.setObjectName("chromeCommandInput")
        self.horizontalLayout_7.addWidget(self.chromeCommandInput)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.chromiumAuto = QtWidgets.QRadioButton(self.layoutWidget)
        self.chromiumAuto.setObjectName("chromiumAuto")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(PreferencesWindow)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.chromiumAuto)
        self.horizontalLayout_8.addWidget(self.chromiumAuto)
        self.chromiumCustom = QtWidgets.QRadioButton(self.layoutWidget)
        self.chromiumCustom.setObjectName("chromiumCustom")
        self.buttonGroup_2.addButton(self.chromiumCustom)
        self.horizontalLayout_8.addWidget(self.chromiumCustom)
        self.chromiumCommandInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.chromiumCommandInput.setMinimumSize(QtCore.QSize(400, 0))
        self.chromiumCommandInput.setObjectName("chromiumCommandInput")
        self.horizontalLayout_8.addWidget(self.chromiumCommandInput)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.firefoxAuto = QtWidgets.QRadioButton(self.layoutWidget)
        self.firefoxAuto.setObjectName("firefoxAuto")
        self.buttonGroup_3 = QtWidgets.QButtonGroup(PreferencesWindow)
        self.buttonGroup_3.setObjectName("buttonGroup_3")
        self.buttonGroup_3.addButton(self.firefoxAuto)
        self.horizontalLayout_9.addWidget(self.firefoxAuto)
        self.firefoxCustom = QtWidgets.QRadioButton(self.layoutWidget)
        self.firefoxCustom.setObjectName("firefoxCustom")
        self.buttonGroup_3.addButton(self.firefoxCustom)
        self.horizontalLayout_9.addWidget(self.firefoxCustom)
        self.firefoxCommandInput = QtWidgets.QLineEdit(self.layoutWidget)
        self.firefoxCommandInput.setMinimumSize(QtCore.QSize(400, 0))
        self.firefoxCommandInput.setObjectName("firefoxCommandInput")
        self.horizontalLayout_9.addWidget(self.firefoxCommandInput)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        spacerItem4 = QtWidgets.QSpacerItem(20, 13, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.cancelButton = QtWidgets.QPushButton(PreferencesWindow)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.saveButton = QtWidgets.QPushButton(PreferencesWindow)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_5.addWidget(self.saveButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(PreferencesWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesWindow)

    def retranslateUi(self, PreferencesWindow):
        _translate = QtCore.QCoreApplication.translate
        PreferencesWindow.setWindowTitle(_translate("PreferencesWindow", "Preferences"))
        self.label_2.setText(_translate("PreferencesWindow", "Proxy ports:"))
        self.label_4.setText(_translate("PreferencesWindow", "Browser commands:"))
        self.label_3.setText(_translate("PreferencesWindow", "Chrome:"))
        self.chromeAuto.setText(_translate("PreferencesWindow", "Auto-detect"))
        self.chromeCustom.setText(_translate("PreferencesWindow", "Custom"))
        self.label_5.setText(_translate("PreferencesWindow", "Chromium"))
        self.chromiumAuto.setText(_translate("PreferencesWindow", "Auto-detect"))
        self.chromiumCustom.setText(_translate("PreferencesWindow", "Custom"))
        self.label_6.setText(_translate("PreferencesWindow", "Firefox"))
        self.firefoxAuto.setText(_translate("PreferencesWindow", "Auto-detect"))
        self.firefoxCustom.setText(_translate("PreferencesWindow", "Custom"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("PreferencesWindow", "Clients"))
        self.cancelButton.setText(_translate("PreferencesWindow", "Cancel"))
        self.saveButton.setText(_translate("PreferencesWindow", "Save"))

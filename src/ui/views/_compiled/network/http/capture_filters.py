# Form implementation generated from reading ui file 'src/ui/views/network/http/capture_filters.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CaptureFilters(object):
    def setupUi(self, CaptureFilters):
        CaptureFilters.setObjectName("CaptureFilters")
        CaptureFilters.resize(485, 313)
        self.verticalLayout = QtWidgets.QVBoxLayout(CaptureFilters)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(CaptureFilters)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.hostSettingDropdown = QtWidgets.QComboBox(CaptureFilters)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hostSettingDropdown.sizePolicy().hasHeightForWidth())
        self.hostSettingDropdown.setSizePolicy(sizePolicy)
        self.hostSettingDropdown.setMinimumSize(QtCore.QSize(205, 0))
        self.hostSettingDropdown.setObjectName("hostSettingDropdown")
        self.hostSettingDropdown.addItem("")
        self.hostSettingDropdown.addItem("")
        self.hostSettingDropdown.addItem("")
        self.horizontalLayout.addWidget(self.hostSettingDropdown)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(CaptureFilters)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.hostsText = QtWidgets.QPlainTextEdit(CaptureFilters)
        self.hostsText.setObjectName("hostsText")
        self.horizontalLayout_2.addWidget(self.hostsText)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.cancelButton = QtWidgets.QPushButton(CaptureFilters)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_5.addWidget(self.cancelButton)
        self.saveButton = QtWidgets.QPushButton(CaptureFilters)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_5.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(CaptureFilters)
        QtCore.QMetaObject.connectSlotsByName(CaptureFilters)

    def retranslateUi(self, CaptureFilters):
        _translate = QtCore.QCoreApplication.translate
        CaptureFilters.setWindowTitle(_translate("CaptureFilters", "Edit Capture Filters"))
        self.label_3.setText(_translate("CaptureFilters", "Host Filter:"))
        self.hostSettingDropdown.setItemText(0, _translate("CaptureFilters", "Disabled"))
        self.hostSettingDropdown.setItemText(1, _translate("CaptureFilters", "Only include hosts:"))
        self.hostSettingDropdown.setItemText(2, _translate("CaptureFilters", "Exclude hosts:"))
        self.label.setText(_translate("CaptureFilters", "Hosts (one host per line, without the port number):"))
        self.cancelButton.setText(_translate("CaptureFilters", "Cancel"))
        self.saveButton.setText(_translate("CaptureFilters", "Save"))

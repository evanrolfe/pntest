# Form implementation generated from reading ui file 'src/ui/views/docker/docker_page.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DockerPage(object):
    def setupUi(self, DockerPage):
        DockerPage.setObjectName("DockerPage")
        DockerPage.resize(1400, 700)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DockerPage)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pageToolbar = QtWidgets.QWidget(DockerPage)
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
        self.verticalLayout_2.addWidget(self.pageToolbar)
        self.dockerSplitter = QtWidgets.QSplitter(DockerPage)
        self.dockerSplitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.dockerSplitter.setObjectName("dockerSplitter")
        self.layoutWidget = QtWidgets.QWidget(self.dockerSplitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 5, 10, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.dockerNetworkDropdown = QtWidgets.QComboBox(self.layoutWidget)
        self.dockerNetworkDropdown.setObjectName("dockerNetworkDropdown")
        self.horizontalLayout.addWidget(self.dockerNetworkDropdown)
        self.refreshButton = QtWidgets.QPushButton(self.layoutWidget)
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.containerTable = HoverableQTableView(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.containerTable.sizePolicy().hasHeightForWidth())
        self.containerTable.setSizePolicy(sizePolicy)
        self.containerTable.setMinimumSize(QtCore.QSize(0, 300))
        self.containerTable.setMaximumSize(QtCore.QSize(16777215, 99999))
        self.containerTable.setObjectName("containerTable")
        self.verticalLayout.addWidget(self.containerTable)
        self.tabs = DockerTabs(self.dockerSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setMinimumSize(QtCore.QSize(500, 300))
        self.tabs.setMaximumSize(QtCore.QSize(16777215, 99999))
        self.tabs.setObjectName("tabs")
        self.verticalLayout_2.addWidget(self.dockerSplitter)

        self.retranslateUi(DockerPage)
        QtCore.QMetaObject.connectSlotsByName(DockerPage)

    def retranslateUi(self, DockerPage):
        _translate = QtCore.QCoreApplication.translate
        DockerPage.setWindowTitle(_translate("DockerPage", "Form"))
        self.label.setText(_translate("DockerPage", "DOCKER"))
        self.label_2.setText(_translate("DockerPage", "Containers"))
        self.label_3.setText(_translate("DockerPage", "Network:"))
from ui.widgets.docker.docker_tabs import DockerTabs
from ui.widgets.qt.hoverable_q_table_view import HoverableQTableView
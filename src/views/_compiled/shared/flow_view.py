# Form implementation generated from reading ui file './src/views/shared/flow_view.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FlowView(object):
    def setupUi(self, FlowView):
        FlowView.setObjectName("FlowView")
        FlowView.resize(590, 678)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FlowView)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(FlowView)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.requestTabs = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestTabs.sizePolicy().hasHeightForWidth())
        self.requestTabs.setSizePolicy(sizePolicy)
        self.requestTabs.setDocumentMode(False)
        self.requestTabs.setObjectName("requestTabs")
        self.requestHeadersTab = QtWidgets.QWidget()
        self.requestHeadersTab.setObjectName("requestHeadersTab")
        self.verticalLayout_6_body = QtWidgets.QVBoxLayout(self.requestHeadersTab)
        self.verticalLayout_6_body.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6_body.setObjectName("verticalLayout_6_body")
        self.requestHeaders = HeadersForm(self.requestHeadersTab)
        self.requestHeaders.setObjectName("requestHeaders")
        self.verticalLayout_6_body.addWidget(self.requestHeaders)
        self.requestTabs.addTab(self.requestHeadersTab, "")
        self.requestBodyTab = QtWidgets.QWidget()
        self.requestBodyTab.setObjectName("requestBodyTab")
        self.verticalLayout_7_body = QtWidgets.QVBoxLayout(self.requestBodyTab)
        self.verticalLayout_7_body.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7_body.setObjectName("verticalLayout_7_body")
        self.requestBody = CodeEditor(self.requestBodyTab)
        self.requestBody.setObjectName("requestBody")
        self.verticalLayout_7_body.addWidget(self.requestBody)
        self.requestTabs.addTab(self.requestBodyTab, "")
        self.stackedWidget = QtWidgets.QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName("stackedWidget")
        self.responseTabs = QtWidgets.QTabWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.responseTabs.sizePolicy().hasHeightForWidth())
        self.responseTabs.setSizePolicy(sizePolicy)
        self.responseTabs.setObjectName("responseTabs")
        self.responseHeadersTab = QtWidgets.QWidget()
        self.responseHeadersTab.setObjectName("responseHeadersTab")
        self.verticalLayout_8_body = QtWidgets.QVBoxLayout(self.responseHeadersTab)
        self.verticalLayout_8_body.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8_body.setObjectName("verticalLayout_8_body")
        self.responseHeaders = HeadersForm(self.responseHeadersTab)
        self.responseHeaders.setObjectName("responseHeaders")
        self.verticalLayout_8_body.addWidget(self.responseHeaders)
        self.responseTabs.addTab(self.responseHeadersTab, "")
        self.responseBodyRawTab = QtWidgets.QWidget()
        self.responseBodyRawTab.setObjectName("responseBodyRawTab")
        self.verticalLayout_4_body = QtWidgets.QVBoxLayout(self.responseBodyRawTab)
        self.verticalLayout_4_body.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4_body.setObjectName("verticalLayout_4_body")
        self.responseRaw = CodeEditor(self.responseBodyRawTab)
        self.responseRaw.setObjectName("responseRaw")
        self.verticalLayout_4_body.addWidget(self.responseRaw)
        self.responseTabs.addTab(self.responseBodyRawTab, "")
        self.responseBodyRenderedTab = QtWidgets.QWidget()
        self.responseBodyRenderedTab.setObjectName("responseBodyRenderedTab")
        self.verticalLayout_body = QtWidgets.QVBoxLayout(self.responseBodyRenderedTab)
        self.verticalLayout_body.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_body.setSpacing(0)
        self.verticalLayout_body.setObjectName("verticalLayout_body")
        self.responseRendered = CodeEditor(self.responseBodyRenderedTab)
        self.responseRendered.setObjectName("responseRendered")
        self.verticalLayout_body.addWidget(self.responseRendered)
        self.responseTabs.addTab(self.responseBodyRenderedTab, "")
        self.stackedWidget.addWidget(self.responseTabs)
        self.loaderWidget = Loader()
        self.loaderWidget.setObjectName("loaderWidget")
        self.stackedWidget.addWidget(self.loaderWidget)
        self.verticalLayout_2.addWidget(self.splitter)

        self.retranslateUi(FlowView)
        self.requestTabs.setCurrentIndex(1)
        self.responseTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FlowView)

    def retranslateUi(self, FlowView):
        _translate = QtCore.QCoreApplication.translate
        FlowView.setWindowTitle(_translate("FlowView", "Form"))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestHeadersTab), _translate("FlowView", "Request"))
        self.requestTabs.setTabText(self.requestTabs.indexOf(self.requestBodyTab), _translate("FlowView", "Body"))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseHeadersTab), _translate("FlowView", "Response"))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyRawTab), _translate("FlowView", "Body"))
        self.responseTabs.setTabText(self.responseTabs.indexOf(self.responseBodyRenderedTab), _translate("FlowView", "Rendered"))
from widgets.shared.code_editor import CodeEditor
from widgets.shared.headers_form import HeadersForm
from widgets.shared.loader import Loader

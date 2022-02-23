from PySide2 import QtCore, QtWidgets

from views._compiled.shared.ui_variables_popup import Ui_VariablesPopup
from models.qt.vars_table_model import VarsTableModel

class VariablesPopup(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(VariablesPopup, self).__init__(parent)

        self.ui = Ui_VariablesPopup()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

        vars = ['1', '2', '3']  # HttpFlow.find_for_table()
        self.table_model = VarsTableModel(vars)
        self.ui.varsTable.setModel(self.table_model)

        # Configure Table
        horizontalHeader = self.ui.varsTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        horizontalHeader.setHighlightSections(False)

        verticalHeader = self.ui.varsTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.varsTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    @QtCore.Slot()
    def save(self):
        print('You clicked save!')
        self.close()

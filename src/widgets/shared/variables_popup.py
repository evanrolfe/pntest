from PyQt6 import QtCore, QtWidgets
from repos.variable_repo import VariableRepo

from views._compiled.shared.variables_popup import Ui_VariablesPopup
from qt_models.vars_table_model import VarsTableModel

class VariablesPopup(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(VariablesPopup, self).__init__(parent)

        self.ui = Ui_VariablesPopup()
        self.ui.setupUi(self)
        self.setModal(True)

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

        # Configure Table
        horizontalHeader = self.ui.varsTable.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setHighlightSections(False)

        verticalHeader = self.ui.varsTable.verticalHeader()
        verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Fixed)
        verticalHeader.setDefaultSectionSize(20)
        verticalHeader.setVisible(False)

        self.ui.varsTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.ui.varsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)

        self.load_variables()

    def save(self):
        for var in self.table_model.variables:
            if not var.is_blank():
                VariableRepo().save(var)
                print(f'saved variable {var.id}')

        self.close()

    def showEvent(self, event):
        self.load_variables()

    def load_variables(self):
        vars = VariableRepo().find_all_global()
        self.table_model = VarsTableModel(vars)
        self.ui.varsTable.setModel(self.table_model)

import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QHeaderView, QAbstractItemView
from PySide2.QtCore import QFile, Slot, QSettings, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSql import QSqlDatabase, QSqlQuery

from views._compiled.network.ui_network_page_widget import Ui_NetworkPageWidget

from lib.app_settings import AppSettings
from models.qt.requests_table_model import RequestsTableModel
from models.request_data import RequestData

class NetworkPageWidget(QWidget):
  send_request_to_editor = Signal(object)

  def __init__(self, *args, **kwargs):
    super(NetworkPageWidget, self).__init__(*args, **kwargs)
    self.ui = Ui_NetworkPageWidget()
    self.ui.setupUi(self)

    # Setup the request model
    self.request_data = RequestData()
    self.request_data.load_requests()
    self.requests_table_model = RequestsTableModel(self.request_data)

    self.ui.requestsTableWidget.setTableModel(self.requests_table_model)
    self.ui.requestsTableWidget.request_selected.connect(self.select_request)
    self.ui.requestsTableWidget.delete_requests.connect(self.delete_requests)
    self.ui.requestsTableWidget.search_text_changed.connect(self.search_requests)
    self.ui.requestsTableWidget.send_request_to_editor.connect(self.send_request_to_editor)

    #self.ui.requestsTableAndViewSplitter.layout().setContentsMargins(0, 0, 0, 0)
    #self.ui.layout().setContentsMargins(0, 0, 0, 0)
    #self.ui.requestsTableAndViewSplitter.layout().setContentsMargins(0, 0, 0, 0)
    #self.ui.requestsTableAndViewSplitter.setStyleSheet("padding: 0px;")
    #self.ui.requestsTableAndViewSplitter.setSpacing(0)
    self.restore_layout_state()

  def restore_layout_state(self):
    settings = AppSettings.get_instance()
    splitterState = settings.get("NetworkPageWidget.requestsTableAndViewSplitterState", None)
    splitterState2 = settings.get("NetworkPageWidget.requestsViewSplitterState", None)

    self.ui.requestsTableAndViewSplitter.restoreState(splitterState)
    self.ui.requestViewWidget.ui.splitter.restoreState(splitterState2)

  def save_layout_state(self):
    splitter_state = self.ui.requestsTableAndViewSplitter.saveState()
    splitter_state2 = self.ui.requestViewWidget.ui.splitter.saveState()

    settings = AppSettings.get_instance()
    settings.save("NetworkPageWidget.requestsTableAndViewSplitterState", splitter_state)
    settings.save("NetworkPageWidget.requestsViewSplitterState", splitter_state2)

  @Slot()
  def select_request(self, selected, deselected):
    if (len(selected.indexes()) > 0):
      selected_id_cols = list(filter(lambda i: i.column() == 0, selected.indexes()))
      selected_id = selected_id_cols[0].data()
      #print(f"SELECTING ID: {selected_id}")
      request = self.request_data.load_request(selected_id)
      self.ui.requestViewWidget.set_request(request)

  @Slot()
  def delete_requests(self, request_ids):
    self.requests_table_model.delete_requests(request_ids)

  @Slot()
  def search_requests(self, search_text):
    print(f'Searching requests! {search_text}')
    self.request_data.set_filter_param('search', search_text)
    self.request_data.load_requests()
    self.requests_table_model.refresh()


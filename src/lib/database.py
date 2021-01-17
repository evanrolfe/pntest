import re

from PySide2.QtSql import QSqlDatabase, QSqlQuery
from orator import DatabaseManager, Model
from models.data.capture_filter import CaptureFilter
from models.data.setting import Setting

NUM_TABLES = 10
SCHEMA_SQL = """CREATE TABLE IF NOT EXISTS requests(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id INTEGER,
  method TEXT,
  url TEXT,
  host TEXT,
  encrypted BOOLEAN,
  http_version TEXT,
  path TEXT,
  ext TEXT,
  websocket_request_id TEXT,
  websocket_sec_key TEXT,

  request_modified BOOLEAN,
  modified_method TEXT,
  modified_url TEXT,
  modified_host TEXT,
  modified_http_version TEXT,
  modified_path TEXT,
  modified_ext TEXT,
  modified_request_headers TEXT,
  modified_request_payload TEXT,

  request_type TEXT,
  response_body_rendered TEXT,
  response_remote_address TEXT,
  response_http_version TEXT,

  request_headers TEXT,
  request_payload TEXT,
  response_status INTEGER,
  response_status_message TEXT,
  response_headers TEXT,
  response_body TEXT,
  response_body_length INTEGER,

  response_modified BOOLEAN,
  modified_response_status INTEGER,
  modified_response_status_message TEXT,
  modified_response_headers TEXT,
  modified_response_body TEXT,
  modified_response_body_length INTEGER,
  modified_response_http_version TEXT,

  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS editor_items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parent_id INTEGER,
  name TEXT NOT NULL,
  item_type TEXT NOT NULL,
  item_id INTEGER,
  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS editor_requests(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parent_id INTEGER,
  method TEXT,
  url TEXT,
  request_headers TEXT,
  request_payload TEXT,

  response_remote_address TEXT,
  response_http_version TEXT,
  response_status INTEGER,
  response_status_message TEXT,
  response_headers TEXT,
  response_body TEXT,
  response_body_length INTEGER,

  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS websocket_messages(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  request_id INTEGER,
  direction TEXT,
  body TEXT,
  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS capture_filters(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filters TEXT NOT NULL,
  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS intercept_filters(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filters TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clients(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  cookies TEXT,
  pages TEXT,
  type TEXT NOT NULL,
  proxy_port INTEGER,
  browser_port INTEGER,
  open BOOLEAN DEFAULT 0,
  created_at INTEGER,
  updated_at INTEGER,
  launched_at INTEGER
);

CREATE TABLE IF NOT EXISTS settings(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT NOT NULL UNIQUE,
  value TEXT NOT NULL,
  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS crawls(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  client_id INTEGER,
  config TEXT,
  status TEXT,
  created_at INTEGER,
  started_at INTEGER,
  finished_at INTEGER
);
"""

class Database:
  def __init__(self, db_path):
    self.db_path = db_path

    config = {
      'default': {
        'driver': 'sqlite',
        'database': db_path
      }
    }

    orator_db = DatabaseManager(config)
    Model.set_connection_resolver(orator_db)

  def load_or_create(self):
    self.db = QSqlDatabase.addDatabase('QSQLITE')
    self.db.setDatabaseName(self.db_path)
    db_result = self.db.open()

    if db_result == True:
      print(f'[Frontend] Loaded database from {self.db_path}')
    else:
      print(f'[Frontend] ERROR could not load database from {self.db_path}')

    db_tables = []
    query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'")
    query.exec_()
    while query.next():
      db_tables.append(query.value(0))

    if (len(db_tables) != NUM_TABLES):
      print(f'[Frontend] database not up-to-date, importing the schema...')
      self.import_schema()

  def import_schema(self):
    query_sql = re.sub(r'\r\n|\n|\r', '', SCHEMA_SQL)
    query_sql = re.sub(r'\s+', ' ', query_sql)
    queries = query_sql.split(';')
    queries = list(filter(None, queries)) # Remove empty strings

    for query_str in queries:
      query = QSqlQuery()
      query.prepare(query_str)
      result = query.exec_()

      if (result == False):
        print(query_str)
        print(query.lastError())

    CaptureFilter.create_defaults()
    Setting.create_defaults()




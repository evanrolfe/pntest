NUM_TABLES = 14
SCHEMA_SQL = """CREATE TABLE IF NOT EXISTS editor_items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parent_id INTEGER,
  name TEXT NOT NULL,
  item_type TEXT NOT NULL,
  item_id INTEGER,
  created_at INTEGER
);

CREATE INDEX index_editor_items_parent_id ON editor_items(parent_id);

CREATE TABLE IF NOT EXISTS clients(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  type TEXT NOT NULL,
  proxy_port INTEGER,
  browser_port INTEGER,
  open BOOLEAN DEFAULT 0,
  created_at INTEGER,
  launched_at INTEGER
);

CREATE TABLE IF NOT EXISTS settings(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  json TEXT NOT NULL,
  created_at INTEGER
);

CREATE TABLE IF NOT EXISTS http_requests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    http_version TEXT NOT NULL,
    headers TEXT,
    content TEXT,
    trailers TEXT,
    timestamp_start REAL,
    timestamp_end REAL,
    host TEXT NOT NULL,
    port INTEGER,
    method TEXT NOT NULL,
    scheme TEXT NOT NULL,
    authority TEXT,
    path TEXT NOT NULL,
    form_data TEXT NOT NULL,
    created_at INTEGER
);

CREATE INDEX index_http_requests_host ON http_requests(host);

CREATE TABLE IF NOT EXISTS http_responses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    http_version TEXT NOT NULL,
    headers TEXT NOT NULL,
    content TEXT,
    timestamp_start REAL,
    timestamp_end REAL,
    status_code INTEGER NOT NULL,
    reason TEXT,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS http_flows(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT,
    client_id INTEGER,
    type TEXT NOT NULL,
    title TEXT,
    request_id INTEGER,
    original_request_id,
    response_id INTEGER,
    original_response_id,
    http_flow_id INTEGER,
    created_at INTEGER NOT NULL
);

CREATE INDEX index_http_flows_uuid ON http_flows(uuid);
CREATE INDEX index_http_flows_type ON http_flows(type);

CREATE TABLE IF NOT EXISTS variables(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  description TEXT,
  source_type TEXT NOT NULL,
  source_id INTEGER,
  created_at INTEGER
);

CREATE INDEX index_variables_key ON variables(key);

CREATE TABLE IF NOT EXISTS websocket_messages(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  http_flow_id INTEGER NOT NULL,
  direction TEXT NOT NULL,
  content TEXT NOT NULL,
  content_original TEXT,
  created_at INTEGER
);

CREATE VIEW v_http_flows_search AS
    SELECT f.id, f.request_id, f.response_id, req.method, req.host, req.path, resp.status_code
    FROM http_flows f
    INNER JOIN http_requests req ON req.id=f.request_id
    LEFT JOIN http_responses resp ON resp.id=f.response_id;

CREATE VIRTUAL TABLE http_flows_fts USING fts5(
    id,
    request_id,
    response_id,
    method,
    host,
    path,
    status_code,
    content='v_http_flows_search',
    content_rowid='id'
)
"""

NUM_TABLES = 11
SCHEMA_SQL = """CREATE TABLE IF NOT EXISTS editor_items(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  parent_id INTEGER,
  name TEXT NOT NULL,
  item_type TEXT NOT NULL,
  item_id INTEGER,
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
    created_at INTEGER,
    updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS http_responses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    http_version TEXT NOT NULL,
    headers TEXT NOT NULL,
    content TEXT,
    timestamp_start REAL,
    timestamp_end REAL,
    status_code INTEGER NOT NULL,
    reason TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS http_flows(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT,
    client_id INTEGER,
    type TEXT NOT NULL,
    request_id INTEGER,
    original_request_id,
    response_id INTEGER,
    original_response_id,
    created_at INTEGER NOT NULL,
    updated_at INTEGER
);

CREATE TABLE IF NOT EXISTS websocket_messages(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  http_flow_id INTEGER NOT NULL,
  direction TEXT NOT NULL,
  content TEXT NOT NULL,
  content_original TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER
);
"""

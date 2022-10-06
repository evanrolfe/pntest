import re
import os
import logging
import sqlite3
import sqlalchemy
import sqlalchemy.orm
from orator import DatabaseManager, Model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.data.settings import Settings
from lib.database_schema import SCHEMA_SQL, NUM_TABLES
from lib.database_model_mapping import register_sqlalchemy_models

# TODO: This class uses two database managers (Orator.DatabaesManager and QSqlDatabase), get rid of
# the unecessary dependency on QSqlDatabase and do everything through Orator

ENABLE_QUERY_LOGGING = False

if ENABLE_QUERY_LOGGING:
    logger = logging.getLogger('orator.connection.queries')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

class Database:
    conn: sqlite3.Connection

    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance():
        # Static access method.
        if Database.__instance is None:
            raise Exception("Database class is a singleton!")
        return Database.__instance

    def __init__(self, db_path):
        self.db_path = db_path

        self.connect_to_db()
        register_sqlalchemy_models()
        # db_url = f"{self.db_path}"
        # self.conn = sqlite3.connect(db_url, isolation_level=None)

        # Virtually private constructor.
        if Database.__instance is not None:
            raise Exception("Database class is a singleton!")
        else:
            Database.__instance = self
    # /Singleton method stuff

    def delete_existing_db(self):
        if os.path.isfile(self.db_path):
            print(f'[Gui] found existing db at {self.db_path}, deleting.')
            os.remove(self.db_path)

    def load_or_create(self):
        db_tables = self.db.select("SELECT name FROM sqlite_master WHERE type='table'")

        if (len(db_tables) != NUM_TABLES):
            print(f'[Gui] database not up-to-date ({len(db_tables)} tables), importing the schema...')
            self.import_schema()

    def connect_to_db(self):
        config = {
            'default': {
                'driver': 'sqlite',
                'database': self.db_path,
                'log_queries': ENABLE_QUERY_LOGGING
            }
        }
        self.db = DatabaseManager(config)
        Model.set_connection_resolver(self.db)

    def register_models(self):
        pass

    def get_session(self):
        db_url = f"sqlite:///{self.db_path}"
        engine = create_engine(db_url)

        session_factory = sessionmaker(bind=engine)
        return scoped_session(session_factory)

    def get_session_factory(self):
        db_url = f"sqlite:///{self.db_path}"
        engine = create_engine(db_url) # , echo="debug"

        session_factory = sessionmaker(bind=engine) # , expire_on_commit=False
        return session_factory

    def import_schema(self):
        query_sql = re.sub(r'\r\n|\n|\r', '', SCHEMA_SQL)
        query_sql = re.sub(r'\s+', ' ', query_sql)
        queries = query_sql.split(';')
        queries = list(filter(None, queries))  # Remove empty strings

        for query_str in queries:
            self.db.insert(query_str)

        # When a flow is inserted:
        trigger1_query = """
            CREATE TRIGGER http_flows_insert AFTER INSERT ON http_flows BEGIN
                INSERT INTO http_flows_fts (id, request_id, method, host, path)
                VALUES (
                    new.id,
                    new.request_id,
                    (SELECT method FROM http_requests WHERE http_requests.id = new.request_id),
                    (SELECT host FROM http_requests WHERE http_requests.id = new.request_id),
                    (SELECT path FROM http_requests WHERE http_requests.id = new.request_id)
                );
            END;
        """
        # When a flow is updated with a response:
        trigger2_query = """
            CREATE TRIGGER http_flows_update AFTER UPDATE ON http_flows BEGIN
                INSERT INTO http_flows_fts (http_flows_fts, rowid, request_id, response_id)
                VALUES ('delete', old.id, old.request_id, old.response_id);

                INSERT INTO http_flows_fts (rowid, response_id, status_code)
                VALUES (
                    new.id,
                    new.response_id,
                    (SELECT status_code FROM http_responses WHERE http_responses.id = new.response_id)
                );
            END;
        """
        # When a flow is deleted:
        trigger3_query = """
            CREATE TRIGGER http_flows_delete AFTER DELETE ON http_flows BEGIN
                INSERT INTO http_flows_fts (http_flows_fts, rowid)
                VALUES ('delete', old.id);
            END;
        """
        # self.db.insert(trigger1_query)
        # self.db.insert(trigger2_query)
        # self.db.insert(trigger3_query)

        Settings.create_defaults()

    def reload_with_new_database(self, new_db_path):
        self.close()
        self.db_path = new_db_path
        self.load_or_create()
        self.connect_to_db()

    def load_new_database(self, new_db_path):
        self.db_path = new_db_path
        self.load_or_create()
        self.connect_to_db()

    def close(self):
        self.db.purge()

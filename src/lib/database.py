import re
import os
import logging
from orator import DatabaseManager, Model

from models.data.capture_filter import CaptureFilter
from models.data.setting import Setting
from lib.database_schema import SCHEMA_SQL, NUM_TABLES

# TODO: This class uses two database managers (Orator.DatabaesManager and QSqlDatabase), get rid of
# the unecessary dependency on QSqlDatabase and do everything through Orator

ENABLE_QUERY_LOGGING = False

if ENABLE_QUERY_LOGGING:
    logger = logging.getLogger('orator.connection.queries')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

class Database:
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

        # Virtually private constructor.
        if Database.__instance is not None:
            raise Exception("Database class is a singleton!")
        else:
            Database.__instance = self
    # /Singleton method stuff

    def delete_existing_db(self):
        if os.path.isfile(self.db_path):
            print('[Gui] found existing db, deleting.')
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

    def import_schema(self):
        query_sql = re.sub(r'\r\n|\n|\r', '', SCHEMA_SQL)
        query_sql = re.sub(r'\s+', ' ', query_sql)
        queries = query_sql.split(';')
        queries = list(filter(None, queries))  # Remove empty strings

        for query_str in queries:
            self.db.insert(query_str)

        CaptureFilter.create_defaults()
        Setting.create_defaults()

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

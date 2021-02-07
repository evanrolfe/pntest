import re
import os
from PySide2 import QtSql
from orator import DatabaseManager, Model

from models.data.capture_filter import CaptureFilter
from models.data.setting import Setting
from lib.database_schema import SCHEMA_SQL, NUM_TABLES

# TODO: This class uses two database managers (Orator.DatabaesManager and QSqlDatabase), get rid of
# the unecessary dependency on QSqlDatabase and do everything through Orator


class Database:
    # Singleton method stuff:
    __instance = None

    @staticmethod
    def get_instance():
        # Static access method.
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self, db_path):
        self.db_path = db_path

        config = {
            'default': {
                'driver': 'sqlite',
                'database': db_path
            }
        }
        self.orator_db = DatabaseManager(config)
        Model.set_connection_resolver(self.orator_db)

        # Virtually private constructor.
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
    # /Singleton method stuff

    def delete_existing_db(self):
        if os.path.isfile(self.db_path):
            print('[Frontend] found existing db, deleting.')
            os.remove(self.db_path)

    def load_or_create(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.db_path)
        db_result = self.db.open()

        if db_result is True:
            print(f'[Frontend] Loaded database from {self.db_path}')
        else:
            print(
                f'[Frontend] ERROR could not load database from {self.db_path}')

        db_tables = []
        query = QtSql.QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'")
        query.exec_()
        while query.next():
            db_tables.append(query.value(0))

        if (len(db_tables) != NUM_TABLES):
            print(f'[Frontend] database not up-to-date, importing the schema...')
            self.import_schema()

    def load_orator_db(self):
        config = {
            'default': {
                'driver': 'sqlite',
                'database': self.db_path
            }
        }
        self.orator_db = DatabaseManager(config)
        Model.set_connection_resolver(self.orator_db)

    def import_schema(self):
        query_sql = re.sub(r'\r\n|\n|\r', '', SCHEMA_SQL)
        query_sql = re.sub(r'\s+', ' ', query_sql)
        queries = query_sql.split(';')
        queries = list(filter(None, queries))  # Remove empty strings

        for query_str in queries:
            query = QtSql.QSqlQuery()
            query.prepare(query_str)
            result = query.exec_()

            if result is False:
                print(query_str)
                print(query.lastError())

        CaptureFilter.create_defaults()
        Setting.create_defaults()

    def reload_with_new_database(self, new_db_path):
        self.close()
        self.db_path = new_db_path
        self.load_or_create()
        self.load_orator_db()

    def load_new_database(self, new_db_path):
        self.db_path = new_db_path
        self.load_or_create()
        self.load_orator_db()

    def close(self):
        self.db.close()
        self.orator_db.purge()

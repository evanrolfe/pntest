import os
import sqlite3

from lib.database_schema import SCHEMA_SQL, NUM_TABLES

class Database:
    # Singleton method stuff:
    __instance = None

    conn: sqlite3.Connection

    @staticmethod
    def get_instance():
        # Static access method.
        if Database.__instance is None:
            raise Exception("Database class is a singleton!")
        return Database.__instance

    def __init__(self, db_path):
        self.db_path = db_path
        # self.delete_existing_db()
        self.connect()
        self.import_schema()
        self.__set_all_clients_closed()

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

    def connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def import_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        db_tables = cursor.fetchall()
        if (len(db_tables) != NUM_TABLES):
            print(f'[Gui] database not up-to-date ({len(db_tables)} tables), importing the schema...')
            self.conn.executescript(SCHEMA_SQL)
            self.conn.commit()

    def reload_with_new_database(self, new_db_path):
        self.close()
        self.db_path = new_db_path
        self.connect()
        self.__set_all_clients_closed()

    def close(self):
        self.conn.close()

    def __set_all_clients_closed(self):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE clients SET open = 0;")
        self.conn.commit()

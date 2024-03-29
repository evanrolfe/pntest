import sqlite3
from typing import Optional

from pypika import Order, QmarkParameter, Query, Table

from entities.client import Client
from repos.base_repo import BaseRepo


class ClientRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('clients')

    def find(self, id: int) -> Optional[Client]:
        row = self.generic_find(id, self.table)
        if row is None:
            return

        # TODO: Use __find_by_query()
        client = Client(**self.row_to_dict(row))
        client.id = row['id']
        client.created_at = row['created_at']
        return client

    def find_all(self) -> list[Client]:
        query = Query.from_(self.table).select('*').orderby(self.table.id, order=Order.desc)
        return self.__find_by_query(query.get_sql())

    def find_by_ids(self, ids: list[int]) -> list[Client]:
        qmark_values = [QmarkParameter() for _ in ids]
        # TODO: Use __find_by_query
        query = Query.from_(self.table).select('*').where(self.table.id.isin(qmark_values))
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql(), ids)
        rows: list[sqlite3.Row] = cursor.fetchall()

        clients = []
        for row in rows:
            client = Client(**self.row_to_dict(row))
            client.id = row['id']
            client.created_at = row['created_at']
            clients.append(client)

        return clients

    def save(self, client: Client):
        if client.id > 0:
            self.generic_update(client, self.table)
        else:
            self.generic_insert(client, self.table)

            # Once we have inserted it and we have an ID, append the ID to the title
            if client.type != 'docker':
                client.title = f'{client.title}-{client.id}'
            self.generic_update(client, self.table)

    def update_all_to_closed(self):
        query = Query.update(self.table).set(self.table.open, 0)
        self.conn.execute(query.get_sql())
        self.conn.commit()

    def get_next_port_available(self) -> int:
        clients = self.find_all()
        proxy_port = Client.PROXY_PORT + len(clients)

        return proxy_port

    def get_used_ports(self) -> list[int]:
        clients = self.find_all()
        return [c.proxy_port for c in clients]

    def __find_by_query(self, sql_query: str) -> list[Client]:
        cursor = self.conn.cursor()
        cursor.execute(sql_query)
        rows: list[sqlite3.Row] = cursor.fetchall()

        clients: list[Client] = []
        for row in rows:
            client = Client(**self.row_to_dict(row))
            client.id = row['id']
            client.created_at = row['created_at']
            clients.append(client)

        return clients

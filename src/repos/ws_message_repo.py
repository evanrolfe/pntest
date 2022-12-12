import json
import sqlite3
from typing import Generic, Optional, Type, TypeVar
from pypika import Query, Table, Field, Order

from models.websocket_message import WebsocketMessage
from repos.base_repo import BaseRepo

# NOTE: This repo should not be accessed directly for saving, only via the HttpFlowRepo
class WsMessageRepo(BaseRepo):
    table: Table

    def __init__(self):
        super().__init__()
        self.table = Table('websocket_messages')

    def find(self, id: int) -> Optional[WebsocketMessage]:
        row = self.generic_find(id, self.table)
        if row is None:
            return

        request = WebsocketMessage(**self.row_to_dict(row))
        request.id = row['id']
        return request

    def save(self, ws_message: WebsocketMessage):
        if ws_message.id > 0:
            self.generic_update(ws_message, self.table)
        else:
            self.generic_insert(ws_message, self.table)

    def delete(self, ws_message: WebsocketMessage):
        self.generic_delete(ws_message, self.table)

    def find_for_table(self, search_text: str) -> list[WebsocketMessage]:
        # TODO: These needs to apply host filters from Settings
        query = Query.from_(self.table).select('*').orderby(self.table.id, order=Order.desc)
        cursor = self.conn.cursor()
        cursor.execute(query.get_sql())
        rows: list[sqlite3.Row] = cursor.fetchall()

        ws_messages: list[WebsocketMessage] = []
        for row in rows:
            message = WebsocketMessage(**self.row_to_dict(row))
            message.id = row['id']
            ws_messages.append(message)

        return ws_messages

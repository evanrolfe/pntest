import sqlite3
from typing import Any, Optional
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, scoped_session, object_session, selectinload

from models.http_flow import HttpFlow
from models.http_request import HttpRequest
from models.http_response import HttpResponse
from models.websocket_message import WebsocketMessage
# from models.client import Client
from lib.database import Database

class HttpFlowRepo:
    session_factory: sessionmaker

    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory = session_factory

    def find(self, id: int) -> Optional[HttpFlow]:
        session = scoped_session(self.session_factory)
        query = select(HttpFlow).where(HttpFlow.id == id).options(selectinload(HttpFlow.websocket_messages))
        result = session.execute(query)
        row = result.fetchone()
        if row is None:
            return None
        print(row.HttpFlow.websocket_messages)
        session.flush()
        return row.HttpFlow

    def find_by(self, where_args: Any) -> Optional[HttpFlow]:
        session = scoped_session(self.session_factory)
        query = select(HttpFlow).where(where_args)
        result = session.execute(query)
        row = result.fetchone()
        if row is None:
            return None
        return row.HttpFlow

    def save(self, flow: HttpFlow, request: Optional[HttpRequest] = None):
        session = scoped_session(self.session_factory)

        if request is not None:
            flow.request = request

        session.add(flow)
        session.commit()

        session.refresh(flow)
        if flow.request is not None:
            session.refresh(flow.request)

        if flow.original_request is not None:
            session.refresh(flow.original_request)

        if flow.client is not None:
            session.refresh(flow.client)

        session.close()

    def add_modified_request(self, flow: HttpFlow, modified_request: HttpRequest):
        if flow.request_id is None:
            raise Exception("cannot call add_modified_request() on a flow which has request_id = NULL")

        session = scoped_session(self.session_factory)

        flow.original_request_id = flow.request_id
        flow.request = modified_request
        session.add(flow)
        session.commit()
        session.refresh(flow)
        session.refresh(flow.request)
        session.refresh(flow.original_request)
        # NOTE: If you dont refresh the client then it seems to "invalidate" the client here
        # TODO: Have a general refresh method which refreshs all the relationships if they are present
        if flow.client is not None:
            session.refresh(flow.client)

        session.close()

    def add_response(self, flow: HttpFlow, response: HttpResponse):
        if flow.request_id is None:
            raise Exception("cannot call add_modified_request() on a flow which has request_id = NULL")

        session = scoped_session(self.session_factory)

        flow.response = response
        session.add(flow)
        session.commit()
        session.refresh(flow)
        session.refresh(flow.response)
        session.close()

    def add_modified_response(self, flow: HttpFlow, modified_response: HttpResponse):
        if flow.response_id is None:
            raise Exception("cannot call add_modified_response() on a flow which has response_id = NULL")

        session = scoped_session(self.session_factory)

        flow.original_response_id = flow.response_id
        flow.response = modified_response
        session.add(flow)
        session.commit()
        session.refresh(flow)
        session.refresh(flow.response)
        session.refresh(flow.original_response)
        session.close()

    def add_websocket_message(self, flow: HttpFlow, ws_message: WebsocketMessage):
        session = scoped_session(self.session_factory)
        session.add(flow)
        session.commit()
        flow.websocket_messages.append(ws_message)
        session.add(flow)
        session.commit()
        session.refresh(flow)
        session.refresh(flow.websocket_messages)
        session.close()

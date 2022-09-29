from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, scoped_session, object_session
from lib.database import Database

from models.http_request import HttpRequest

class HttpRequestRepo:
    session_factory: sessionmaker

    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory = session_factory

    def save(self, request: HttpRequest):
        session = scoped_session(self.session_factory)
        session.add(request)
        session.commit()
        session.refresh(request)
        session.close()

    def find(self, id: int) -> Optional[HttpRequest]:
        session = scoped_session(self.session_factory)
        query = select(HttpRequest).where(HttpRequest.id == id)
        result = session.execute(query)
        row = result.fetchone()
        if row is None:
            return None

        return row.HttpRequest

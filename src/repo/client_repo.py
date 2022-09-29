from sqlalchemy.orm import sessionmaker, scoped_session, object_session
from lib.database import Database

from models.client import Client

class ClientRepo:
    session_factory: sessionmaker

    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory = session_factory

    def save(self, client: Client):
        session = scoped_session(self.session_factory)
        session.add(client)
        session.commit()
        session.refresh(client)
        session.close()


from lib.database import Database
from models.data.orator_model import OratorModel

class HttpFlowSearch(OratorModel):
    __table__ = 'http_flows_fts'

    @classmethod
    def search(cls, search_term: str) -> list[int]:
        database = Database.get_instance()
        results = database.db.select("SELECT * FROM http_flows_fts WHERE http_flows_fts MATCH ?;", [search_term])

        return [r.id for r in results]

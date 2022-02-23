from __future__ import annotations

from models.data.orator_model import OratorModel

class Variable(OratorModel):
    __table__ = 'variables'

    SOURCE_TYPE_GLOBAL = 'global'
    SOURCE_TYPE_REQUEST = 'http_request'

    def item(self):
        if self.source_type == self.SOURCE_TYPE_GLOBAL:
            return None

    def is_blank(self):
        id = getattr(self, 'id', None)
        key = getattr(self, 'key', None)
        value = getattr(self, 'value', None)
        description = getattr(self, 'description', None)

        return id is None and key is None and value is None and description is None

    @classmethod
    def all_global(cls):
        return cls.where('source_type', '=', cls.SOURCE_TYPE_GLOBAL).order_by('id', 'asc').get()

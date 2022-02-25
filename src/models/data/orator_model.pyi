from __future__ import annotations

from typing import Any
from orator import Model
from orator.orm import Builder

# Orator does not come with type stub files, so we have to maintain our own

class OratorModel(Model):
    @classmethod
    def where(cls, arg1: str, arg2: str, arg3: Any) -> Builder:
        pass

    @classmethod
    def order_by(cls, arg1: str, arg2: str) -> Builder:
        pass

    @classmethod
    def count(cls) -> int:
        pass

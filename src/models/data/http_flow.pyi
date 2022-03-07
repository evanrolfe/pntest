from __future__ import annotations

from typing import Optional, Any
from models.data.orator_model import OratorModel
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse

class HttpFlow(OratorModel):
    # Database columns:
    id: int
    uuid: Optional[str]
    client_id: int
    type: str
    title: Optional[str]
    request_id: int
    original_request_id: Optional[int]
    response_id: Optional[int]
    original_response_id: Optional[int]
    http_flow_id: int
    created_at: int
    updated_at: Optional[int]

    # Associations:
    request: HttpRequest
    response: Optional[HttpResponse]

    original_request: Optional[HttpRequest]
    original_response: Optional[HttpResponse]

    # Constants:
    TYPE_PROXY: str
    TYPE_EDITOR: str
    TYPE_EDITOR_EXAMPLE: str
    TYPE_EDITOR_FUZZ: str

    # Orator Methods:
    def save(self) -> HttpFlow:
        pass

    # Class & Instance Methods:
    @classmethod
    def find_for_table(cls) -> list[HttpFlow]:
        pass

    @classmethod
    def create_for_editor(cls, type: str) -> HttpFlow:
        pass

    def is_example(self) -> bool:
        pass

    def request_modified(self) -> bool:
        pass

    def response_modified(self) -> bool:
        pass

    def modified(self) -> bool:
        pass

    def has_response(self) -> bool:
        pass

    def values_for_table(self) -> list[Any]:
        pass

    def duplicate_for_editor(self) -> HttpFlow:
        pass

    def duplicate_for_example(self, request: HttpRequest, response: HttpResponse) -> HttpFlow:
        pass

    def duplicate_for_fuzz_example(self, num: int) -> HttpFlow:
        pass

    def modify_request(self, modified_method: str, modified_path: str, modified_headers: dict[str, str], modified_content: str) -> None:
        pass

    def modify_response(self, modified_status_code: int, modified_headers: dict[str, str], modified_content: str) -> None:
        pass

    def modify_latest_websocket_message(self, modified_content: str) -> None:
        pass

    def reload(self) -> HttpFlow:
        pass

    def get_host_and_port(self, host) -> list[Any]:
        pass

    def is_editable(self) -> bool:
        pass

    def make_request(self) -> HttpResponse:
        pass

    def make_request_and_save(self) -> None:
        pass

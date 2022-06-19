from typing import Any, TypedDict

# Types which are used by both the main process and the proxy processes, unfortunately this code needs
# to be stored in src/proxy, otherwise you get an "ImportError: attempted relative import with no known parent package"
# If you have a solution to this please let me know or submit a pull request

class CaptureFilterSettings(TypedDict):
    host_list: list[str]
    host_setting: str
    path_list: list[str]
    path_setting: str

class DisplayFilterSettings(TypedDict):
    host_list: list[str]
    host_setting: str
    path_list: list[str]
    path_setting: str

class SettingsJson(TypedDict):
    capture_filters: CaptureFilterSettings
    display_filters: DisplayFilterSettings

class ProxyRequest(TypedDict):
    http_version: str
    headers: list[tuple[str, str]]
    content: bytes
    trailers: Any
    timestamp_start: float
    timestamp_end: float
    host: str
    port: int
    method: str
    scheme: str
    authority: str
    path: str
    flow_uuid: str
    type: str
    client_id: int
    intercepted: bool

class ProxyResponse(TypedDict):
    http_version: str
    headers: list[tuple[str, str]]
    content: bytes
    trailers: Any
    timestamp_start: float
    timestamp_end: float
    status_code: int
    reason: str
    flow_uuid: str
    type: str
    intercepted: bool

class ProxyWebsocketMessage(TypedDict):
    type: str
    flow_uuid: str
    direction: str
    content: str
    intercepted: bool

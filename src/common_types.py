from typing import TypedDict

# Types which are used by both the main process and the proxy processes

class CaptureFilterSettings(TypedDict):
    host_list: list[str]
    host_setting: str
    path_list: list[str]
    path_setting: str
    ext_list: list[str]
    ext_setting: str

class SettingsJson(TypedDict):
    capture_filters: CaptureFilterSettings

from typing import TypedDict

# Types which are used by both the main process and the proxy processes, unfortunately this code needs
# to be stored in src/proxy, otherwise you get an "ImportError: attempted relative import with no known parent package"
# If you have a solution to this please let me know or submit a pull request

class CaptureFilterSettings(TypedDict):
    host_list: list[str]
    host_setting: str
    path_list: list[str]
    path_setting: str
    ext_list: list[str]
    ext_setting: str

class SettingsJson(TypedDict):
    capture_filters: CaptureFilterSettings

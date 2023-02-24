from __future__ import annotations
from typing import TypedDict

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

class ProjectSettings(TypedDict):
    capture_filters: CaptureFilterSettings
    display_filters: DisplayFilterSettings

def get_default_project_settings() -> ProjectSettings:
    capture_filters: CaptureFilterSettings = {
        'host_list': [],
        'host_setting': '',
        'path_list': [],
        'path_setting': '',
    }
    display_filters: DisplayFilterSettings = {
        'host_list': [],
        'host_setting': '',
        'path_list': [],
        'path_setting': '',
    }
    settings_json: ProjectSettings = {
        'capture_filters': capture_filters,
        'display_filters': display_filters,
    }
    return settings_json

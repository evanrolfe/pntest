from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from PyQt6 import QtCore
from typing import Any, Optional, TypedDict

class AppSettings(TypedDict):
    proxy_ports_available: list[int]
    browser_commands: dict[str, str]
    network_layout: str
    main_window_geometry: Optional[QtCore.QByteArray]
    editor_page_splitter_state: Optional[QtCore.QByteArray]
    request_edit_page_splitter_state: Optional[QtCore.QByteArray]
    fuzz_edit_page_splitter_state: Optional[QtCore.QByteArray]

def get_default_app_settings() -> AppSettings:
    defaults: AppSettings = {
        'proxy_ports_available': [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089],
        'browser_commands': {},
        'network_layout': 'vertical1',
        'main_window_geometry': None,
        'editor_page_splitter_state': None,
        'request_edit_page_splitter_state': None,
        'fuzz_edit_page_splitter_state': None,
    }
    return defaults

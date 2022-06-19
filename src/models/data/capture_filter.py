from __future__ import annotations
import json
from typing import Optional, Any
import inflection

from orator import accessor
from models.data.orator_model import OratorModel

# TODO: Remove this class as its unused
class CaptureFilter(OratorModel):
    id: int
    filters: str
    created_at: Optional[int]
    updated_at: Optional[int]

    DEFAULT_CAPTURE_FILTERS = {
        'hostList': [],
        'hostSetting': '',
        'pathList': [],
        'pathSetting': '',
        'extList': [],
        'extSetting': '',
        'navigationRequests': True
    }

    @classmethod
    def create_defaults(cls) -> CaptureFilter:
        capture_filter = CaptureFilter()
        capture_filter.id = 1
        capture_filter.filters = json.dumps(cls.DEFAULT_CAPTURE_FILTERS)
        capture_filter.save()
        return capture_filter

    @accessor
    def host_list(self) -> list[str]:
        return self.parsed_filters('hostList')

    @accessor
    def host_setting(self) -> str:
        return self.parsed_filters('hostSetting')

    @accessor
    def path_list(self) -> list[str]:
        return self.parsed_filters('pathList')

    @accessor
    def path_setting(self) -> str:
        return self.parsed_filters('pathSetting')

    @accessor
    def ext_list(self) -> list[str]:
        return self.parsed_filters('extList')

    @accessor
    def ext_setting(self) -> str:
        return self.parsed_filters('extSetting')

    @accessor
    def navigation_requests(self) -> bool:
        return self.parsed_filters('navigationRequests')

    def parsed_filters(self, value: str = None) -> Any:
        parsed_filters = json.loads(self.filters)

        if value is None:
            return parsed_filters
        else:
            return parsed_filters[value]

    def set_filters(self, filters: dict[str, str]) -> None:
        current_filters = self.parsed_filters()

        for key, value in filters.items():
            camel_case_key = inflection.camelize(key, False)
            current_filters[camel_case_key] = value

        self.filters = json.dumps(current_filters)

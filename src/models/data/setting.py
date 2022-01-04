from typing import Optional
from models.data.orator_model import OratorModel

class Setting(OratorModel):
    id: int
    key: str
    value: str
    created_at: Optional[int]
    updated_at: Optional[int]

    @classmethod
    def create_defaults(cls):
        setting = Setting()
        setting.key = 'interceptEnabled'
        setting.value = '0'
        setting.save()

    @classmethod
    def intercept_enabled(cls):
        setting = Setting.where('key', '=', 'interceptEnabled').first_or_fail()
        return (setting.value == '1')

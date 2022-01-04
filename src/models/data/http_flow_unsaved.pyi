from models.data.http_flow import HttpFlow

class HttpFlowUnsaved(HttpFlow):
    def save(self) -> HttpFlow:
        pass

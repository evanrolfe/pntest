from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest

class HttpFlowUnsaved(HttpFlow):
    def __init__(self, *args, **kwargs):
        super(HttpFlowUnsaved, self).__init__(*args, **kwargs)

        self.type = HttpFlow.TYPE_EDITOR
        self.request = HttpRequest()
        self.request.set_blank_values_for_editor()

        self.response = None
        self.examples = []

    def save(self):
        self.request.save()

        saved_flow = HttpFlow()
        saved_flow.type = self.type
        saved_flow.request_id = self.request.id
        saved_flow.save()

        return saved_flow

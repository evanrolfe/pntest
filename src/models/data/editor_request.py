import json
from orator import Model

from widgets.shared.request_headers_form import RequestHeadersForm

class EditorRequest(Model):
    __table__ = 'editor_requests'
    # Default values:
    __attributes__ = {'method': 'GET'}

    def duplicate(self):
        editor_request = EditorRequest()
        editor_request.method = self.method
        editor_request.url = self.url
        editor_request.request_headers = self.request_headers
        editor_request.request_payload = self.request_payload
        editor_request.response_remote_address = self.response_remote_address
        editor_request.response_http_version = self.response_http_version
        editor_request.response_status = self.response_status
        editor_request.response_status_message = self.response_status_message
        editor_request.response_headers = self.response_headers
        editor_request.response_body = self.response_body
        editor_request.response_body_length = self.response_body_length
        return editor_request

    def children(self):
        return EditorRequest.where('parent_id', '=', self.id).order_by('created_at', 'desc').get()

    def delete_resursive(self):
        for child in self.children():
            child.delete_resursive()

        self.delete()

    def get_request_headers(self):
        if self.request_headers is None:
            return None

        return json.loads(self.request_headers)

    def set_request_headers(self, headers_dict):
        self.request_headers = json.dumps(headers_dict)

    def overwrite_calculated_headers(self):
        calc_text = RequestHeadersForm.CALCULATED_TEXT
        headers = self.get_request_headers()

        if headers.get('host'):
            headers['host'] = calc_text

        if headers.get('content-length'):
            headers['content-length'] = calc_text

        self.set_request_headers(headers)

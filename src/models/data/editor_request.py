import json
from orator import Model

from widgets.editor.request_headers_form import RequestHeadersForm

class EditorRequest(Model):
  __table__ = 'editor_requests'

  def children(self):
    return EditorRequest.where('parent_id', '=', self.id).order_by('created_at', 'desc').get()

  def delete_resursive(self):
    for child in self.children():
      child.delete_resursive()

    self.delete()

  def get_request_headers(self):
    if self.request_headers == None:
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

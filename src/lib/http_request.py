from requests import Request, Session

from widgets.editor.request_headers_form import RequestHeadersForm

class HttpRequest:
  def __init__(self, method, url, headers, body):
    self.method = method
    self.url = url
    self.headers = headers
    self.body = body

  def send(self):
    print(f'Requesting {self.method} {self.url}')
    session = Session()
    request = Request(self.method, self.url, headers = self.parsed_headers(), data = self.body)
    prepped_request = session.prepare_request(request)

    self.response = session.send(prepped_request)
    return self.response

  def parsed_headers(self):
    parsed_headers = {}

    for key, value in self.headers.items():
      if value != RequestHeadersForm.CALCULATED_TEXT:
        parsed_headers[key] = value

    return parsed_headers

import json

# TODO: Move this to an Orator model in models/data/network_request.py
class Request:
  def __init__(self, attributes):
    self.id = attributes.get('id')
    self.client_id = attributes.get('client_id')
    self.method = attributes.get('method')
    self.host = attributes.get('host')
    self.path = attributes.get('path')
    self.encrypted = (attributes.get('encrypted') == 1)
    self.http_version = attributes.get('http_version')
    self.request_headers = attributes.get('request_headers')
    self.request_payload = attributes.get('request_payload')
    self.request_type = attributes.get('request_type')

    self.request_modified = (attributes.get('request_modified') == 1)
    self.modified_method = attributes.get('modified_method')
    self.modified_url = attributes.get('modified_url')
    self.modified_host = attributes.get('modified_host')
    self.modified_http_version = attributes.get('modified_http_version')
    self.modified_path = attributes.get('modified_path')
    self.modified_ext = attributes.get('modified_ext')
    self.modified_request_headers = attributes.get('modified_request_headers')
    self.modified_request_payload = attributes.get('modified_request_payload')

    self.response_headers = attributes.get('response_headers')
    self.response_status = attributes.get('response_status')
    self.response_status_message = attributes.get('response_status_message')
    self.response_http_version = attributes.get('response_http_version')
    self.response_body = attributes.get('response_body')
    self.response_body_rendered = attributes.get('response_body_rendered')

    self.response_modified = (attributes.get('response_modified') == 1)
    self.modified_response_status = attributes.get('modified_response_status')
    self.modified_response_status_message = attributes.get('modified_response_status_message')
    self.modified_response_http_version = attributes.get('modified_response_http_version')
    self.modified_response_headers = attributes.get('modified_response_headers')
    self.modified_response_body = attributes.get('modified_response_body')
    self.modified_response_body_length = attributes.get('modified_response_body_length')

  def is_editable(self):
    return (self.method != None and self.method != '')

  def url(self):
    if self.encrypted:
      return f'https://{self.host}{self.path}'
    else:
      return f'http://{self.host}{self.path}'

  def modified(self):
    if (self.request_modified == True or self.response_modified == True):
      return 'Yes'
    else:
      return ''

  def has_response(self):
    return (self.response_status != '')

  def request_headers_parsed(self):
    http_message = f'{self.method} {self.path} HTTP/{self.http_version}\n'
    http_message += self.__parse_headers_json(self.request_headers)

    if (self.request_payload):
      http_message += f'\n{self.request_payload}'

    return http_message

  def request_headers_modified_parsed(self):
    http_message = f'{self.modified_method} {self.modified_path} HTTP/{self.modified_http_version}\n'
    http_message += self.__parse_headers_json(self.modified_request_headers)

    if (self.modified_request_payload):
      http_message += f'\n{self.modified_request_payload}'

    return http_message

  def response_headers_parsed(self):
    if (self.has_response() == False):
      return 'No response.'

    http_response = f'HTTP/{self.response_http_version} {self.response_status} {self.response_status_message}\n'
    http_response += self.__parse_headers_json(self.response_headers)

    return http_response

  def response_headers_modified_parsed(self):
    http_response = f'HTTP/{self.modified_response_http_version} {self.modified_response_status} {self.modified_response_status_message}\n'
    http_response += self.__parse_headers_json(self.modified_response_headers)

    return http_response

  def response_body_for_preview(self):
    if not self.response_body_rendered:
      return self.response_body
    else:
      return self.response_body_rendered

  def __parse_headers_json(self, headers_json):
    try:
      output = ''
      headers = json.loads(headers_json)

      for key, value in headers.items():
        output += f'{key}: {value}\n'

      return output

    except json.decoder.JSONDecodeError:
      return ''

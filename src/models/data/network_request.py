import json
from orator import Model

class NetworkRequest(Model):
    __table__ = 'requests'
    __fillable__ = ['*']

    @classmethod
    def search(cls, params):
        return cls.all()

    def is_editable(self):
        return (self.method is not None and self.method != '')

    def get_url(self):
        if self.encrypted:
            return f'https://{self.host}{self.path}'
        else:
            return f'http://{self.host}{self.path}'

    def get_modified_request(self):
        new_request = NetworkRequest()
        new_request.id = self.id
        new_request.client_id = self.client_id
        new_request.encrypted = self.encrypted
        new_request.request_modified = self.request_modified
        new_request.response_modified = self.response_modified
        new_request.request_type = self.request_type
        new_request.response_body_rendered = self.response_body_rendered
        new_request.response_remote_address = self.response_remote_address

        new_request.method = self.modified_method
        new_request.url = self.modified_url
        new_request.host = self.modified_host
        new_request.http_version = self.modified_http_version
        new_request.path = self.modified_path
        new_request.ext = self.modified_ext
        new_request.request_headers = self.modified_request_headers
        new_request.request_payload = self.modified_request_payload

        new_request.response_status = self.modified_response_status
        new_request.response_status_message = self.modified_response_status_message
        new_request.response_headers = self.modified_response_headers
        new_request.response_body = self.modified_response_body
        new_request.response_body_length = self.modified_response_body_length
        new_request.response_http_version = self.modified_response_http_version

        return new_request

    def modified(self):
        return self.request_modified == 1 or self.response_modified == 1

    def modified_str(self):
        if self.modified():
            return 'Yes'
        else:
            return ''

    def has_response(self):
        return (self.response_status != '')

    def get_request_headers(self):
        if self.request_headers is None:
            return None
        return json.loads(self.request_headers)

    def get_request_header_line(self):
        return f'{self.method} {self.path} HTTP/{self.http_version}'

    def get_response_headers(self):
        if self.response_headers is None:
            return None
        return json.loads(self.response_headers)

    def get_response_header_line(self):
        if self.response_status is None:
            return 'No response'
        else:
            return f'HTTP/{self.response_http_version} {self.response_status} {self.response_status_message}\n'

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
        if self.has_response() is False:
            return 'No response.'

        http_response = f'HTTP/{self.response_http_version} {self.response_status} {self.response_status_message}\n'
        http_response += self.__parse_headers_json(self.response_headers)

        return http_response

    def response_headers_modified_parsed(self):
        http_response = f'HTTP/{self.modified_response_http_version}'
        http_response += f' {self.modified_response_status}'
        http_response += f' {self.modified_response_status_message}\n'
        http_response += self.__parse_headers_json(self.modified_response_headers)

        return http_response

    def response_body_for_preview(self):
        if not self.response_body_rendered:
            return self.response_body
        else:
            return self.response_body_rendered

    def __parse_headers_json(self, headers_json):
        if headers_json is None:
            return ''

        try:
            output = ''
            headers = json.loads(headers_json)

            for key, value in headers.items():
                output += f'{key}: {value}\n'

            return output

        except json.decoder.JSONDecodeError:
            return ''

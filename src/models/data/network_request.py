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

    def url(self):
        if self.encrypted:
            return f'https://{self.host}{self.path}'
        else:
            return f'http://{self.host}{self.path}'

    def modified(self):
        if self.request_modified is True or self.response_modified is True:
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

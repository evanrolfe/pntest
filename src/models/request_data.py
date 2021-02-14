from PySide2 import QtSql

from models.data.network_request import NetworkRequest

# TODO: Move this logic into the NetworkRequest model and remove the use of QtSql
class RequestData:
    SEARCHABLE_COLUMNS = ['id', 'method', 'host', 'path']

    def __init__(self):
        self.requests = []
        self.filter_params = {}

    def set_filter_param(self, key, value):
        self.filter_params[key] = value

    def load_requests(self):
        self.requests = []

        search_term = self.filter_params.get('search')
        if search_term:
            conditions_list = list(
                map(lambda x: f'{x} LIKE "%{search_term}%"', self.SEARCHABLE_COLUMNS))
            conditions_str = ' OR '.join(conditions_list)

            query_str = f'SELECT * FROM requests WHERE {conditions_str} ORDER BY id DESC'
        else:
            query_str = "SELECT * FROM requests ORDER BY id DESC"

        query = QtSql.QSqlQuery(query_str)

        while query.next():
            request = self.request_from_query_result(query)
            self.requests.append(request)

        print(f'found {len(self.requests)} requests with query:\n{query_str}')

    def request_from_query_result(self, query):
        request = NetworkRequest()
        request.id = query.value('id')
        request.client_id = query.value('client_id')
        request.method = query.value('method')
        request.host = query.value('host')
        request.path = query.value('path')
        request.encrypted = query.value('encrypted')
        request.http_version = query.value('http_version')
        request.request_headers = query.value('request_headers')
        request.request_payload = query.value('request_payload')
        request.request_type = query.value('request_type')
        request.request_modified = query.value('request_modified')
        request.modified_method = query.value('modified_method')
        request.modified_url = query.value('modified_url')
        request.modified_host = query.value('modified_host')
        request.modified_http_version = query.value('modified_http_version')
        request.modified_path = query.value('modified_path')
        request.modified_ext = query.value('modified_ext')
        request.modified_request_headers = query.value('modified_request_headers')
        request.modified_request_payload = query.value('modified_request_payload')
        request.response_headers = query.value('response_headers')
        request.response_status = query.value('response_status')
        request.response_status_message = query.value('response_status_message')
        request.response_http_version = query.value('response_http_version')
        request.response_body = query.value('response_body')
        request.response_body_rendered = query.value('response_body_rendered')
        request.response_modified = query.value('response_modified')
        request.modified_response_status = query.value('modified_response_status')
        request.modified_response_status_message = query.value('modified_response_status_message')
        request.modified_response_http_version = query.value('modified_response_http_version')
        request.modified_response_headers = query.value('modified_response_headers')
        request.modified_response_body = query.value('modified_response_body')
        request.modified_response_body_length = query.value('modified_response_body_length')

        return request

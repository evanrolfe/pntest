from PySide2.QtSql import QSqlDatabase, QSqlQuery

from models.request import Request

class RequestData:
  SEARCHABLE_COLUMNS = ['id', 'method', 'host', 'path']

  def __init__(self):
    self.requests = []
    self.filter_params = {}

  def update_request(self, new_request):
    for i, request in enumerate(self.requests):
      if request.id == new_request.id:
        self.requests[i] = new_request

  def delete_requests(self, request_ids):
    # HACK: Using bindValue with a list of ids did not work so we have to call bindValue
    # for each id individually inside a loop
    question_marks = ', '.join(['?' for _ in range(len(request_ids))])

    query = QSqlQuery()
    query.prepare(f"DELETE FROM requests WHERE id IN ({question_marks})")

    for i, request_id in enumerate(request_ids):
      query.bindValue(i, request_id)

    result = query.exec_()

    if (result == False):
      print("THERE WAS AN ERROR WITH THE SQL QUERY!")

    self.requests = list(filter(lambda r: r.id not in request_ids, self.requests))

  def get_index_of(self, request_id):
    for i, r in enumerate(self.requests):
      if r.id == request_id:
        return i

  def set_filter_param(self, key, value):
    self.filter_params[key] = value

  def load_requests(self):
    self.requests = []

    search_term = self.filter_params.get('search')
    if search_term:
      conditions_list = list(map(lambda x: f'{x} LIKE "%{search_term}%"', self.SEARCHABLE_COLUMNS))
      conditions_str = ' OR '.join(conditions_list)

      query_str = f'SELECT * FROM requests WHERE {conditions_str} ORDER BY id DESC'
    else:
      query_str = "SELECT * FROM requests ORDER BY id DESC"

    query = QSqlQuery(query_str)

    while query.next():
      request = self.request_from_query_result(query)
      self.requests.append(request)

    print(f'found {len(self.requests)} requests with query:\n{query_str}')

  def load_request(self, request_id):
    query = QSqlQuery()
    query.prepare("SELECT * FROM requests WHERE id=:id")
    query.bindValue(":id", request_id)
    query.exec_()
    query.next()

    return self.request_from_query_result(query)

  def request_from_query_result(self, query):
    attrs = {
      'id': query.value('id'),
      'client_id': query.value('client_id'),
      'method': query.value('method'),
      'host': query.value('host'),
      'path': query.value('path'),
      'encrypted': query.value('encrypted'),
      'http_version': query.value('http_version'),
      'request_headers': query.value('request_headers'),
      'request_payload': query.value('request_payload'),
      'request_type': query.value('request_type'),

      'request_modified': query.value('request_modified'),
      'modified_method': query.value('modified_method'),
      'modified_url': query.value('modified_url'),
      'modified_host': query.value('modified_host'),
      'modified_http_version': query.value('modified_http_version'),
      'modified_path': query.value('modified_path'),
      'modified_ext': query.value('modified_ext'),
      'modified_request_headers': query.value('modified_request_headers'),
      'modified_request_payload': query.value('modified_request_payload'),

      'response_headers': query.value('response_headers'),
      'response_status': query.value('response_status'),
      'response_status_message': query.value('response_status_message'),
      'response_http_version': query.value('response_http_version'),
      'response_body': query.value('response_body'),
      'response_body_rendered': query.value('response_body_rendered'),

      'response_modified': query.value('response_modified'),
      'modified_response_status': query.value('modified_response_status'),
      'modified_response_status_message': query.value('modified_response_status_message'),
      'modified_response_http_version': query.value('modified_response_http_version'),
      'modified_response_headers': query.value('modified_response_headers'),
      'modified_response_body': query.value('modified_response_body'),
      'modified_response_body_length': query.value('modified_response_body_length'),
    }

    return Request(attrs)

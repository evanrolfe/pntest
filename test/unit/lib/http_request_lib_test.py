from lib.http_request import HttpRequest
from models.data.variable import Variable
from support.factories import factory

class TestHttpRequest:
    def test_from_state_and_get_state(self, database, cleanup_database):
        factory(Variable, 'global').create(key='method', value='POST')
        factory(Variable, 'global').create(key='host', value='localhost')
        factory(Variable, 'global').create(key='apiVersion', value='v2')
        factory(Variable, 'global').create(key='account_name', value='MyAccount')
        factory(Variable, 'global').create(key='apiToken', value='0123456789')

        method = '${var:method}'
        url = 'http://${var:host}/api/${var:apiVersion}/accounts'
        headers = {'X-Api-Token': '${var:apiToken}'}
        body = '{"name": "${var:account_name}", "type": "account"}'
        request = HttpRequest(method, url, headers, body)

        assert request.method == 'POST'
        assert request.url == 'http://localhost/api/v2/accounts'
        assert request.body == '{"name": "MyAccount", "type": "account"}'
        assert request.headers == {'X-Api-Token': '0123456789'}

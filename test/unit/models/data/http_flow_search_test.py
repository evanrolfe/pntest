from models.data.http_flow import HttpFlow
from models.data.http_flow_search import HttpFlowSearch
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from support.factories import factory

class TestHttpFlowSearch:
    def test_find_for_table_host(self, database, cleanup_database):
        # Flow 1:
        http_request1 = factory(HttpRequest, 'proxy').make()
        http_request1.save()

        http_flow1 = factory(HttpFlow, 'proxy').make(request_id=http_request1.id, client_id=1)
        http_flow1.save()

        # Flow 2:
        http_request2 = factory(HttpRequest, 'proxy').make()
        http_request2.save()

        http_response2 = factory(HttpResponse, 'http_response').make()
        http_response2.save()

        http_flow2 = factory(HttpFlow, 'proxy').make(request_id=http_request2.id, response_id=http_response2.id, client_id=1)
        http_flow2.save()

        search_results = HttpFlowSearch.search('"syn"*')

        # for result in search_results:
        #     print(f'id: {result["id"]}, request_id: {result["request_id"]}, response_id: {result["response_id"]}, method: {result["method"]}, host: {result["host"]}, path: {result["path"]}, status_code: {result["status_code"]}')

        assert len(search_results) == 2

        search_results2 = HttpFlowSearch.search('"xxx"*')
        assert len(search_results2) == 0

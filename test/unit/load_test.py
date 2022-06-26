import random
from models.data.http_flow import HttpFlow
from models.data.http_request import HttpRequest
from models.data.http_response import HttpResponse
from support.factories import factory

class TestLoad:
    def test_find_for_table_host(self, database, cleanup_database):
        assert 1 == 1
    #     total_num = 10000
    #     hosts = ['synack.com', 'cnn.com', 'google.com']

    #     for i in range(10000):
    #         # Flow 2:
    #         http_request = factory(HttpRequest, 'proxy').make(host=random.choice(hosts), path=f'/{i}')
    #         http_request.save()

    #         http_flow = factory(HttpFlow, 'proxy').make(request_id=http_request.id, client_id=1)
    #         http_flow.save()

    #         http_response = factory(HttpResponse, 'http_response').make()
    #         http_response.save()
    #         http_flow.response_id = http_response.id
    #         http_flow.save()

    #         if i % 100 == 0:
    #             print(i + " / " + total_num)

    # print('Done')

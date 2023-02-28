import uuid

from support.factories.client_factory import ClientFactory
from support.factories.http_request_factory import HttpRequestFactory
from support.factories.http_response_factory import HttpResponseFactory

from entities.client import Client
from entities.http_flow import HttpFlow
from repos.client_repo import ClientRepo
from repos.http_flow_repo import HttpFlowRepo


def create_multiple_flows() -> list[HttpFlow]:
    client = Client(title="test client!", type="browser", proxy_port=8080)
    ClientRepo().save(client)
    flow1 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        client=client,
        request=HttpRequestFactory.build(path="/modified1"),
        original_request=HttpRequestFactory.build(path="/original1"),
        response=HttpResponseFactory.build(status_code=404, content="not found"),
        original_response=HttpResponseFactory.build(status_code=200, content="original"),
    )
    flow2 = HttpFlow(
        uuid=str(uuid.uuid4()),
        type="proxy",
        client=client,
        request=HttpRequestFactory.build(path="/modified2"),
        original_request= HttpRequestFactory.build(path="/original2"),
        response=HttpResponseFactory.build(status_code=200, content="<html>hello world</html>"),
        original_response=HttpResponseFactory.build(status_code=200, content="<html>original</html>"),
    )
    HttpFlowRepo().save(flow1)
    HttpFlowRepo().save(flow2)

    return [flow1, flow2]

class TestHttpFlowRepo:
    def test_saving_and_retrieving_a_flow(self, database, cleanup_database):
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client: Client = ClientFactory.build()
        client_repo.save(client)

        flow = HttpFlow(
            type="proxy",
            client=client,
            request=HttpRequestFactory.build(path="/original")
        )
        http_flow_repo.save(flow)

        assert flow.id is not None
        assert flow.type == "proxy"

    def test_finding_a_flow_that_doesnt_exist(self, database, cleanup_database):
        http_flow_repo = HttpFlowRepo()
        result = http_flow_repo.find(0)

        assert result is None

    def test_updating_a_flow(self, database, cleanup_database):
        http_flow_repo = HttpFlowRepo()
        client_repo = ClientRepo()

        client: Client = ClientFactory.build()
        client_repo.save(client)

        flow = HttpFlow(
            type="proxy",
            client=client,
            request=HttpRequestFactory.build(path="/original")
        )
        http_flow_repo.save(flow)

        assert flow.id is not None

        flow.created_at = 2
        flow.type = 'editor'
        http_flow_repo.save(flow)

        flow2 = http_flow_repo.find(flow.id)
        assert flow2 is not None
        assert flow.id == flow.id
        assert flow.created_at == 2
        assert flow.type == 'editor'

    def test_find_by_uuid(self, database, cleanup_database):
        _, flow2 = create_multiple_flows()
        if flow2.uuid is None:
            assert False

        result = HttpFlowRepo().find_by_uuid(flow2.uuid)

        assert result is not None
        assert result.id == flow2.id

    def test_delete(self, database, cleanup_database):
        _, flow2 = create_multiple_flows()

        HttpFlowRepo().delete(flow2)

        results, total_count = HttpFlowRepo().find_for_table("", 0, 20)

        assert total_count == 1
        assert len(results) == 1

    def test_null_character_error(self, database, cleanup_database):
        request = HttpRequestFactory.build(path="/one", content = 'PING\x00')

        flow = HttpFlow(
            type="editor",
            request=request,
        )
        # Needs to be done twice so generic_update() is also tested
        HttpFlowRepo().save(flow)
        HttpFlowRepo().save(flow)

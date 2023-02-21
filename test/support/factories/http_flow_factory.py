import factory

from entities.http_flow import HttpFlow
factory.django.DjangoModelFactory
class HttpFlowFactory(factory.Factory):
    class Meta:
        model = HttpFlow

    class Params:
        with_req = factory.Trait(
            # TODO
        )

        with_req_resp = factory.Trait(
            # TODO
        )


    # TODO: Create a client


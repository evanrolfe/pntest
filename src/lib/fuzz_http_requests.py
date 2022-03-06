from models.data.http_flow import HttpFlow

class FuzzHttpRequests:
    flow: HttpFlow

    def __init__(self, flow: HttpFlow):
        self.flow = flow

    def start(self):
        # 1. Load all payloads
        payloads = self.flow.request.payload_files()
        for p in payloads:
            p.load_values()

        # TODO: Handle payloads of varying length by trimming the longer ones
        n = payloads[0].num_items

        # 2. Loop through each combination
        for i in range(0, n):
            payload_values = {}
            for payload in payloads:
                payload_values[payload.key] = payload.values[i]

            # 2.1 Generate an HttpFlow + HttpRequest
            example_flow = self.flow.duplicate_for_fuzz_example()

            # 2.2 Replace the ${payload:usernames} values in the request
            example_flow.request.apply_payload_values(payload_values)

            print(i)
            print(example_flow.request.form_data['content'])

            # 2.3 Make the request

            # 2.4 Save the response
        return

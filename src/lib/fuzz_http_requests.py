from PySide2 import QtCore
from typing import cast
from lib.background_worker import WorkerSignals
from models.data.http_flow import HttpFlow

class FuzzHttpRequests:
    flow: HttpFlow
    cancelled: bool

    def __init__(self, flow: HttpFlow):
        self.flow = flow
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def start(self, signals: WorkerSignals):
        # 1. Load all payloads
        payloads = self.flow.request.payload_files()
        for p in payloads:
            p.load_values()

        # TODO: Handle payloads of varying length by trimming the longer ones
        n = payloads[0].num_items

        # 2. Loop through each combination
        for i in range(0, n):
            if self.cancelled:
                break

            payload_values = {}
            for payload in payloads:
                payload_values[payload.key] = payload.values[i]

            # 2.1 Generate an HttpFlow + HttpRequest
            example_flow = self.flow.duplicate_for_fuzz_example(i + 1)

            # 2.2 Replace the ${payload:usernames} values in the request
            example_flow.request.apply_payload_values(payload_values)

            # 2.3 Make the request
            example_flow.request.save()
            example_flow.make_request_and_save()

            # 2.4 Emit a signal
            cast(QtCore.SignalInstance, signals.response_received).emit(example_flow)

        return

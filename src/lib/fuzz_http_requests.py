import time
import random
from PyQt6 import QtCore
import itertools
from typing import cast
from lib.background_worker import WorkerSignals
from models.data.http_flow import HttpFlow
from models.data.http_request import FuzzFormData, HttpRequest

class FuzzHttpRequests:
    flow: HttpFlow
    fuzz_data: FuzzFormData
    cancelled: bool

    def __init__(self, flow: HttpFlow):
        self.flow = flow
        self.cancelled = False

        fuzz_data = self.flow.request.fuzz_data()
        if fuzz_data is None:
            return
        self.fuzz_data = fuzz_data

    def cancel(self) -> None:
        self.cancelled = True

    def start(self, signals: WorkerSignals) -> None:
        if self.fuzz_data['fuzz_type'] == HttpRequest.FUZZ_TYPE_KEYS[0]:
            self.start_one_to_one(signals)
        elif self.fuzz_data['fuzz_type'] == HttpRequest.FUZZ_TYPE_KEYS[1]:
            self.start_cartesian(signals)

    def start_one_to_one(self, signals: WorkerSignals) -> None:
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
            signals.response_received.emit(example_flow)

            # Optionally sleep
            self.sleep_inbetween_requests()

    def start_cartesian(self, signals: WorkerSignals) -> None:
        # 1. Load all payloads
        payloads = self.flow.request.payload_files()
        for p in payloads:
            p.load_values()

        values = [p.values for p in payloads]
        cart_product = itertools.product(*values)

        # 2. Loop through each combination
        for i, product in enumerate(cart_product):
            if self.cancelled:
                break

            payload_values = {}
            for j, payload in enumerate(payloads):
                payload_values[payload.key] = product[j]

            # 2.1 Generate an HttpFlow + HttpRequest
            example_flow = self.flow.duplicate_for_fuzz_example(i + 1)

            # 2.2 Replace the ${payload:usernames} values in the request
            example_flow.request.apply_payload_values(payload_values)

            # 2.3 Make the request
            example_flow.request.save()
            example_flow.make_request_and_save()

            # 2.4 Emit a signal
            signals.response_received.emit(example_flow)

            # Optionally sleep
            self.sleep_inbetween_requests()


    def sleep_inbetween_requests(self):
        if self.fuzz_data['delay_type'] == HttpRequest.DELAY_TYPE_KEYS[0]: # Disabled
            return
        elif self.fuzz_data['delay_type'] == HttpRequest.DELAY_TYPE_KEYS[1]: # Fixed
            duration = self.fuzz_data['delay_secs']
            if duration is None:
                return
            time.sleep(int(duration))

        elif self.fuzz_data['delay_type'] == HttpRequest.DELAY_TYPE_KEYS[2]: # Range
            min = self.fuzz_data['delay_secs_min']
            max = self.fuzz_data['delay_secs_max']
            if min is None:
                min = 0
            if max is None:
                return

            duration = random.randint(int(min), int(max))
            print("Sleeping for ", duration, " secs")
            time.sleep(duration)

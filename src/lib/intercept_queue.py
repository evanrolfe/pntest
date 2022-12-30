import json
from PyQt6 import QtCore
from lib.process_manager import ProcessManager
from models.http_flow import HttpFlow

# InterceptQueue takes in multiple flows from multiple proxies, it puts them all on a queue
# and waits for a decision one at a time from the intercept page

class InterceptQueue(QtCore.QObject):
    decision_required = QtCore.pyqtSignal(HttpFlow)
    intercept_changed = QtCore.pyqtSignal(bool)
    queue_empty = QtCore.pyqtSignal()
    queue: list[HttpFlow]

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.queue = []
        self.awaiting_decision = False

        self.process_manager = ProcessManager.get_instance()
        self.process_manager.flow_intercepted.connect(self.flow_intercepted)
        self.process_manager.intercept_changed.connect(self.intercept_changed)

    def flow_intercepted(self, flow: HttpFlow):
        print(f'[InterceptQueue] received intercepted flow {flow.uuid}')
        self.queue.append(flow)

        if not self.awaiting_decision:
            self.request_decision(flow)

    def request_decision(self, flow: HttpFlow):
        self.awaiting_decision = True
        self.decision_required.emit(flow)

    def forward_flow(self, flow: HttpFlow, intercept_response: bool):
        self.process_manager.forward_flow(flow, intercept_response)
        self.__pop_queue_and_await_next_decision()

    def drop_flow(self, flow: HttpFlow):
        self.process_manager.drop_flow(flow)
        self.__pop_queue_and_await_next_decision()

    def forward_all(self):
        self.process_manager.forward_all()
        self.queue = []
        self.queue_empty.emit()

    def enabled(self) -> bool:
        return self.process_manager.intercept_enabled

    def toggle_intercept_enabled(self):
        self.process_manager.toggle_intercept_enabled()

    # Private Methods

    def __pop_queue_and_await_next_decision(self):
        self.queue.pop(0)
        self.awaiting_decision = False

        if len(self.queue) == 0:
            self.queue_empty.emit()
            return

        next_flow = self.queue[0]
        self.request_decision(next_flow)

    def __print_queue(self):
        print(f'[InterceptQueue] queue is now:')
        queue_uuids = [f.uuid for f in self.queue]
        print(json.dumps(queue_uuids))

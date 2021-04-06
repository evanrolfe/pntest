import json
from PySide2 import QtCore
from lib.process_manager import ProcessManager
from models.data.http_flow import HttpFlow

# InterceptQueue takes in multiple flows from multiple proxies, it puts them all on a queue
# and waits for a decision one at a time from the intercept page

class InterceptQueue(QtCore.QObject):
    decision_required = QtCore.Signal(HttpFlow)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.queue = []
        self.awaiting_decision = False

        self.process_manager = ProcessManager.get_instance()
        self.process_manager.flow_intercepted.connect(self.flow_intercepted)

    @QtCore.Slot()
    def flow_intercepted(self, flow):
        self.queue.append(flow)
        print(f'[InterceptQueue] received intercepted flow {flow.uuid}')

        if not self.awaiting_decision:
            self.request_decision(flow)

    def request_decision(self, flow):
        self.awaiting_decision = True
        self.decision_required.emit(flow)

    def forward_flow(self, flow):
        self.process_manager.forward_intercepted_flow(flow)
        self.queue.pop(0)
        self.awaiting_decision = False

        if len(self.queue) > 0:
            next_flow = self.queue[0]
            self.request_decision(next_flow)

    def __print_queue(self):
        print(f'[InterceptQueue] queue is now:')
        queue_uuids = [f.uuid for f in self.queue]
        print(json.dumps(queue_uuids))

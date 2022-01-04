from PySide2 import QtGui

from models.data.editor_item import EditorItem
from models.data.http_flow_unsaved import HttpFlowUnsaved

class EditorItemUnsaved(EditorItem):
    def __init__(self, *args, **kwargs):
        super(EditorItemUnsaved, self).__init__(*args, **kwargs)

        self.name = 'Untitled'
        self.item_type = EditorItem.TYPE_HTTP_FLOW
        self.http_flow = HttpFlowUnsaved()

    def item(self):
        return self.http_flow

    def save(self):
        saved_flow = self.http_flow.save()

        saved_editor_item = EditorItem()
        saved_editor_item.name = self.name
        saved_editor_item.item_type = self.item_type
        saved_editor_item.item_id = saved_flow.id
        saved_editor_item.save()

        return saved_editor_item

    def icon(self):
        # if self.item_type == self.TYPE_HTTP_FLOW:
        #     icon_methods = ['get', 'put', 'patch', 'delete', 'post', 'options', 'head']
        #     method = self.item().request.method.lower()
        #     if method not in icon_methods:
        #         method = 'other'
        method = 'get'
        return QtGui.QIcon(QtGui.QPixmap(f":/icons/dark/methods/{method}.png"))

from orator import Model
from PySide2 import QtGui

from models.data.http_flow import HttpFlow

class EditorItem(Model):
    __table__ = 'editor_items'

    TYPE_HTTP_FLOW = 'http_flow'
    TYPE_DIR = 'dir'

    def duplicate(self):
        if self.item_type != self.TYPE_HTTP_FLOW:
            print('WARNING - cannot duplicate editor items which arent http_flows')
            return

        flow = self.item().duplicate_for_editor()
        flow.save()

        editor_item = EditorItem()
        editor_item.name = self.name
        editor_item.item_type = self.item_type
        editor_item.item_id = flow.id
        return editor_item

    def children(self):
        return EditorItem.where('parent_id', '=', self.id).order_by('item_type', 'asc').get()

    def delete_everything(self):
        self.delete_resursive()
        if self.item() is not None:
            self.item().delete()

    def delete_resursive(self):
        for child in self.children():
            child.delete_resursive()

        self.delete()

    def item(self):
        if self.item_type == self.TYPE_HTTP_FLOW:
            return HttpFlow.where('id', '=', self.item_id).first()

    def save(self, *args, **kwargs):
        item_id = getattr(self, 'item_id', None)

        if self.item_type == self.TYPE_HTTP_FLOW and item_id is None:
            flow = HttpFlow.create_for_editor()
            self.item_id = flow.id

        super(EditorItem, self).save(*args, **kwargs)

    @classmethod
    def create_for_http_flow(cls, flow):
        editor_item = EditorItem()
        editor_item.name = 'new request'
        editor_item.item_type = cls.TYPE_HTTP_FLOW
        editor_item.item_id = flow.id
        editor_item.save()

        return editor_item

    def icon(self):
        if self.item_type == self.TYPE_HTTP_FLOW:
            icon_methods = ['get', 'put', 'patch', 'delete', 'post', 'options', 'head']
            method = self.item().request.method.lower()
            if method not in icon_methods:
                method = 'other'

            return QtGui.QIcon(f":/icons/dark/methods/{method}.png")

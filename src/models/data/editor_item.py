from orator import Model
from PySide2 import QtGui

from models.data.editor_request import EditorRequest
from models.data.network_request import NetworkRequest

class EditorItem(Model):
    __table__ = 'editor_items'

    # NOTE: This only works for type=request
    def duplicate(self):
        editor_request = self.item().duplicate()
        editor_request.save()

        editor_item = EditorItem()
        editor_item.name = self.name
        editor_item.item_type = self.item_type
        editor_item.item_id = editor_request.id
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
        if self.item_type == 'request':
            return EditorRequest.where('id', '=', self.item_id).first()

    def save(self, *args, **kwargs):
        item_id = getattr(self, 'item_id', None)

        if self.item_type == 'request' and item_id is None:
            request = EditorRequest()
            request.save()
            print(f'Created request id {request.id}')
            self.item_id = request.id

        super(EditorItem, self).save(*args, **kwargs)

    @classmethod
    def create_from_network_request(cls, network_request):
        # Reload the request from the database:
        network_request = NetworkRequest.find(network_request.id)

        editor_request = EditorRequest()
        editor_request.method = network_request.method
        editor_request.url = network_request.url()
        editor_request.request_headers = network_request.request_headers
        editor_request.request_payload = network_request.request_payload
        editor_request.overwrite_calculated_headers()
        editor_request.save()

        editor_item = EditorItem()
        editor_item.name = 'new request'
        editor_item.item_type = 'request'
        editor_item.item_id = editor_request.id
        editor_item.save()
        print('Saved')
        return editor_item

    def icon(self):
        if self.item_type == 'request':
            icon_methods = ['get', 'put', 'patch', 'delete', 'post', 'options', 'head']

            method = self.item().method.lower()
            if method not in icon_methods:
                method = 'other'

            return QtGui.QIcon(f":/icons/dark/methods/{method}.png")

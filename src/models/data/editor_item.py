from orator import Model
from models.data.editor_request import EditorRequest
from models.request_data import RequestData

class EditorItem(Model):
  __table__ = 'editor_items'

  def children(self):
    return EditorItem.where('parent_id', '=', self.id).order_by('item_type', 'asc').get()

  def delete_everything(self):
    self.delete_resursive()
    if self.item() != None:
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

    if self.item_type == 'request' and item_id == None:
      request = EditorRequest()
      request.save()
      print(f'Created request id {request.id}')
      self.item_id = request.id

    super(EditorItem, self).save(*args, **kwargs)

  @classmethod
  def create_from_network_request(cls, network_request):
    # Reload the request from the database:
    request_data = RequestData()
    network_request = request_data.load_request(network_request.id)

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



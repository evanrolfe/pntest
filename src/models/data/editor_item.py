from __future__ import annotations
from typing import Optional
from PyQt6 import QtGui

from models.data.orator_model import OratorModel
from models.data.http_flow import HttpFlow

class EditorItem(OratorModel):
    __table__ = 'editor_items'

    TYPE_HTTP_FLOW = 'http_flow'
    TYPE_DIR = 'dir'
    TYPE_FUZZ = 'fuzz'

    def duplicate(self):
        if self.item_type != self.TYPE_HTTP_FLOW:
            print('WARNING - cannot duplicate editor items which arent http_flows')
            return

        original_flow = self.item()
        if original_flow is None:
            return

        flow = original_flow.duplicate_for_editor()
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
        item = self.item()

        if item is not None:
            item.delete()

    def delete_resursive(self):
        for child in self.children():
            child.delete_resursive()

        self.delete()

    def item(self):
        if self.item_type in [self.TYPE_HTTP_FLOW, self.TYPE_FUZZ]:
            return HttpFlow.where('id', '=', self.item_id).first()

    def save(self, *args, **kwargs):
        item_id = getattr(self, 'item_id', None)

        if self.item_type in [self.TYPE_HTTP_FLOW, self.TYPE_FUZZ] and item_id is None:
            if self.item_type == self.TYPE_FUZZ:
                type = HttpFlow.TYPE_EDITOR_FUZZ
            else:
                type = HttpFlow.TYPE_EDITOR

            flow = HttpFlow.create_for_editor(type)
            self.item_id = flow.id

        return super(EditorItem, self).save(*args, **kwargs)

    @classmethod
    def create_for_http_flow(cls, flow):
        editor_item = EditorItem()
        editor_item.name = 'new request'
        editor_item.item_type = cls.TYPE_HTTP_FLOW
        editor_item.item_id = flow.id
        editor_item.save()

        return editor_item

    # TODO: This should probably be moved elsewhere cause the data model shouldn't have QtGui as a dependency
    def icon(self) -> QtGui.QIcon:
        if self.item_type == self.TYPE_FUZZ:
            return QtGui.QIcon(f"assets:icons/dark/methods/fuzz.png")

        if self.item_type == self.TYPE_HTTP_FLOW:
            icon_methods = ['get', 'put', 'patch', 'delete', 'post', 'options', 'head']

            item = self.item()
            if item is None:
                raise Exception("No item found for editor item")

            method = item.request.method.lower()
            if method not in icon_methods:
                method = 'other'

            return QtGui.QIcon(f"assets:icons/dark/methods/{method}.png")

        raise Exception("No item found for editor item")

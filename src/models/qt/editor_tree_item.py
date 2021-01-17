import re

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QTreeWidgetItem

class EditorTreeItem(object):
  def __init__(self, label, editor_item = None, is_dir = False, parent=None):
    self.parent = parent
    self.label = label
    self.is_dir = is_dir
    self.editor_item = editor_item
    self.childItems = []

  @classmethod
  def from_editor_item(cls, editor_item):
    is_dir = (editor_item.item_type == 'dir')
    return cls(editor_item.name, editor_item, is_dir)

  def data(self):
    return self.label

  def child(self, row):
    try:
      return self.childItems[row]
    except IndexError:
      return None

  def childCount(self):
    return len(self.childItems)

  def childNumber(self):
    if self.parent != None:
      return self.parent.childItems.index(self)

    return 0

  def childIndicatorPolicy(self):
    return QTreeWidgetItem.ShowIndicator

  def columnCount(self):
    return 1

  def sortChildren(self):
    self.childItems = sorted(self.childItems, key=lambda x: (not x.is_dir, x.label))

  def insertChild(self, child_item):
    self.childItems.append(child_item)
    child_item.parent = self

    if self.editor_item != None:
      child_item.editor_item.parent_id = self.editor_item.id
      child_item.editor_item.save()
    else:
      child_item.editor_item.parent_id = None
      child_item.editor_item.save()

    self.sortChildren()

  def insertChildren(self, child_items):
    for item in  child_items:
      self.insertChild(item)

  def removeChildren(self, position, count, delete=False):
    if position < 0 or position + count > len(self.childItems):
      return False

    for row in range(count):
      removed_item = self.childItems.pop(position)
      if delete:
        removed_item.editor_item.delete_everything()

    return True

  def setLabel(self, label):
    # TODO: Remove *'s becuase they will mess with the modified indicator
    self.label = label
    self.editor_item.name = label
    self.editor_item.save()

    return True

  def icon(self):
    if self.is_dir:
      return None
    else:
      return QIcon(":/icons/dark/icons8-document-50.png")


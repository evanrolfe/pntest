from PySide2 import QtCore, QtGui, QtWidgets

class HtmlHighlighter(QtGui.QSyntaxHighlighter):
  def highlightBlock(self, text):
    self.text = text

    format1 = QtGui.QTextCharFormat()
    format1.setFontWeight(QtGui.QFont.Bold)
    format1.setForeground(QtCore.Qt.darkMagenta)

    format2 = QtGui.QTextCharFormat()
    format2.setFontWeight(QtGui.QFont.Bold)
    format2.setForeground(QtCore.Qt.darkBlue)

    self.apply_rule("<.+>", format1)
    self.apply_rule("\".+\"", format2)

  def apply_rule(self, pattern, class_format):
    expression = QtCore.QRegExp(pattern)
    index = expression.indexIn(self.text)

    while index >= 0:
      length = expression.matchedLength()
      self.setFormat(index, length, class_format)
      index = expression.indexIn(self.text, index + length)

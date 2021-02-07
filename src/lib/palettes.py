from PySide2 import QtCore
from PySide2.QtGui import QPalette, QColor

class Palettes:
    @staticmethod
    def dark():
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QPalette.Base, QColor('#464643'))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QtCore.Qt.black)
        palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QPalette.Text, QtCore.Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)

        # Disabled:
        palette.setColor(QPalette.Disabled,
                         QPalette.WindowText, QColor('#E9E9E9'))
        palette.setColor(QPalette.Disabled, QPalette.Button, QColor('#464643'))

        return palette

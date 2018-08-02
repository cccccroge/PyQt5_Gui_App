import sys
from PyQt5 import QtWidgets

class tool(QtWidgets.QToolBar):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # Actions have been initialize in menu, just add them
        parent.toolBar = parent.addToolBar(self.tr("common tools"))
        toolBar = parent.toolBar

        toolBar.setMovable(False)
        toolBar.addAction(parent.actions["openDir"])
        toolBar.addAction(parent.actions["importExcel"])
        toolBar.addSeparator()
        toolBar.addAction(parent.actions["viewExcel"])
        toolBar.addSeparator()
        toolBar.addAction(parent.actions["loadTemplate"])
        toolBar.addAction(parent.actions["saveTemplate"])


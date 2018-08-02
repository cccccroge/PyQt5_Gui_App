import sys
from PyQt5 import QtWidgets

class status(QtWidgets.QStatusBar):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.statusBar = parent.statusBar()

    def show_default(self):
        self.statusBar.showMessage("Ready")



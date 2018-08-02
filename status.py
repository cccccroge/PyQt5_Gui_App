import sys
from PyQt5 import QtWidgets

class status(QtWidgets.QStatusBar):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        parent.statusBar().showMessage("就緒")





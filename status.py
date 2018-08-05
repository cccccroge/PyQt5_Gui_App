import sys
from PyQt5 import QtWidgets

class status(QtWidgets.QStatusBar):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        parent.hintLabel = QtWidgets.QLabel()
        parent.hintLabel.setText("就緒")
        parent.progressBar = QtWidgets.QProgressBar()
        parent.progressBar.setVisible(False)
        parent.statusBar().addPermanentWidget(parent.hintLabel)
        parent.statusBar().addPermanentWidget(parent.progressBar)

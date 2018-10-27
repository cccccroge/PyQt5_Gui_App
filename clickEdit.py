from PyQt5 import QtWidgets, QtCore
from globalUsed import fieldRowHeight

class clickEdit(QtWidgets.QLineEdit):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setFixedSize(100, fieldRowHeight)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(False)
        self.setDisabled(True)
        self.setReadOnly(True)

    def focusOutEvent(self, QFocusEvent):
        print("focus out")
        self.setDisabled(True)
        self.setReadOnly(True)

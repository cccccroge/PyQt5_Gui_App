from PyQt5 import QtWidgets

class list(QtWidgets.QListWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.parent.list = self

    def showFile(self, _targetName):
        names = self.parent.colNamesSet[_targetName]

        self.clear()
        for n in names:
            item = QtWidgets.QListWidgetItem()
            item.setText(n)
            self.addItem(item)
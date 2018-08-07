from PyQt5 import QtWidgets

class connectButton(QtWidgets.QPushButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setText(self.tr("建立聯結"))
        self.setAcceptDrops(True)
        self.pressed.connect(self.on_pressed)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        print("data is: " + event.mimeData().text())
        event.acceptProposedAction()

    def on_pressed(self):
        print("connect!")


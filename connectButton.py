from PyQt5 import QtWidgets

class connectButton(QtWidgets.QPushButton):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        #self.colToConnect

        self.setText(self.tr("建立聯結"))
        self.setAcceptDrops(True)
        self.pressed.connect(self.on_pressed)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            # TODO: add a regExpress check condition
            event.acceptProposedAction()

    def dropEvent(self, event):
        # Take out the info
        text = event.mimeData().text()
        pos1 = text.find(",")
        pos2 = text.rfind(",")
        fileName = text[:pos1]
        sheetName = text[pos1+1:pos2]
        colName = text[pos2+1:]

        t = (fileName, sheetName, colName)
        self.parent.connectedCols.append(t)

        event.acceptProposedAction()

    def on_pressed(self):
        print("connect!")


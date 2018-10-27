from PyQt5 import QtWidgets

class dropEdit(QtWidgets.QLineEdit):
    def __init__(self, _showTextOnDrop, **kwargs):
        super().__init__(**kwargs)

        self.showTextOnDrop = _showTextOnDrop
        self.colSource = None
        

    ####################
    #    Overloadeds
    ####################
    
    # DragEnter: check if is plain text

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/plain"):
            # TODO: add a regExpress check condition
            event.acceptProposedAction()


    # Drop: parse text to store tuple

    def dropEvent(self, event):
        # Take out the info
        text = event.mimeData().text()
        pos1 = text.find(",")
        pos2 = text.rfind(",")
        fileName = text[:pos1]
        sheetName = text[pos1+1:pos2]
        colName = text[pos2+1:]

        # Store tuple to block
        self.colSource = fileName, sheetName, colName

        # Set text
        if self.showTextOnDrop:
            self.setText(colName)

        print("drop source: {0}".format(self.colSource))
        event.acceptProposedAction()


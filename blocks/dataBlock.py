from PyQt5 import QtWidgets
import block
import pandas as pd

class dataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("資料")

        self.disableBtn()
        self.setAcceptDrops(True)


    def generateOut(self, input, inputColSrc, graph):
        # Invalid input
        if type(input) != pd.core.frame.DataFrame \
            and type(input) != pd.core.series.Series:
                return None, None
        
        # More than one row: use first row
        if type(input) == pd.core.frame.DataFrame:
            input = input.iloc[0]

        
        fromNode = inputColSrc[0:2]
        toNode = self.colSource[0:2]
        ret = graph.shortest_path(fromNode, toNode)
        # Not connected
        if ret == False:
            return None, None

        # Find path from inputColSrc to the block's colSrc
        print("find path from {0} to {1}:".format(fromNode, toNode))
        print(ret)
        return "好啊", None



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

        print("drop source: {0}".format(self.colSource))
        event.acceptProposedAction()


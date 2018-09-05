from PyQt5 import QtWidgets
import block
import pandas as pd
import numpy as np
import networkx as nx

class multiDataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("多重資料")

        self.disableBtn()
        self.setAcceptDrops(True)


    def generateOut(self, input, inputColSrc, graph):
        # No input
        if input is None:
            return None, None, "-->資料輸入為空"

        # Invalid input
        if type(input) != pd.core.frame.DataFrame \
            and type(input) != pd.core.series.Series:
                return None, None, "-->資料不是'表格'或'列'"
        
        # No data
        if input.empty:
            print("in dataBlock: input is {0}".format(input))
            return None, None, "-->資料表(/列)為空表(/列)"

        fromNode = inputColSrc[0:2]
        toNode = self.colSource[0:2]

        # Not same file: impossible to get multiData
        if fromNode != toNode:
            return None, None, "-->前者方塊必須與之相同才能抓取多筆資料"

        # Get the final value
        blkColSrc = self.colSource[2]

        #isStr = pd.api.types.is_string_dtype(curRow[blkColSrc])
        #print("DB isStr = {0}".format(isStr))
        #if isStr:
        #    data = str(curRow.at[blkColSrc])
        #else:
        data = input[[blkColSrc]]

        return data, self.colSource, ""


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


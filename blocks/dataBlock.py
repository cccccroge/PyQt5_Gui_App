from PyQt5 import QtWidgets
import block
import pandas as pd
import networkx as nx

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
                print("輸出時某'資料'方塊之輸入無效")
                return None, None
        
        # More than one row: use first row
        if type(input) == pd.core.frame.DataFrame:
            input = input.iloc[0]

        
        fromNode = inputColSrc[0:2]
        toNode = self.colSource[0:2]
        if (fromNode not in graph) or (toNode not in graph):
            print("輸出時出現檔案關聯失敗：某一資料表不曾被連結")
            return None, None

        if nx.has_path(graph, fromNode, toNode) == False:
            print("輸出時出現檔案關聯失敗：兩個資料表間不存在有效連結")
            return None, None

        pathNodes = nx.shortest_path(graph, fromNode, toNode)

        # Find last connected row from inputColSrc to the block's colSrc
        curRow = input
        for i in range(len(pathNodes) - 1):
            # each relationship find another row
            preNode = pathNodes[i]
            postNode = pathNodes[i + 1]
            pre2postPath = graph[preNode][postNode]["common"]
            print("pre2postPath = {0}".format(pre2postPath))
            preCol = pre2postPath[0]
            postCol = pre2postPath[1]
            
            preVal = curRow.at[preCol]
            postFile = self.parent.srcFiles[postNode]
            try:
                rows = postFile.loc[postFile[postCol] == preVal]
            except KeyError:
                print("輸出時，檔案關聯期間連結錯誤：兩個資料表的共同欄位值不同步")
                return None, None

            curRow = rows.iloc[0]

        # Get the final value
        blkColSrc = self.colSource[2]
        data = curRow.at[blkColSrc]
        return data, self.colSource


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


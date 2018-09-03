from PyQt5 import QtWidgets
import block
import pandas as pd
import numpy as np
import networkx as nx

class dataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("資料")

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
            return None, None, "-->資料表(/列)為空表(/列)"

        # More than one row: use first row
        if type(input) == pd.core.frame.DataFrame:
            input = input.iloc[0]

        
        fromNode = inputColSrc[0:2]
        toNode = self.colSource[0:2]

        # Same file: don't care graph
        if fromNode == toNode:
            colName = self.colSource[2]

            #isStr = pd.api.types.is_string_dtype(input[colName])
            #print("DB isStr = {0}".format(isStr))
            #if isStr:
            #    data = str(input.at[colName])
            #else:
            data = input.at[colName]

            return data, self.colSource, ""

        # Failed to relate
        absence1 = str(fromNode) if (fromNode not in graph) else ""
        absence2 = str(toNode) if (toNode not in graph) else ""
        if absence1 == "" and absence2 != "":
            return None, None, "-->" + absence2 + "不曾被連結"
        if absence1 != "" and absence2 == "":
            return None, None, "-->" + absence1 + "不曾被連結"
        if absence1 != "" and absence2 != "":
            return None, None, "-->" + absence1 + "和" + absence2 + "皆不曾被連結"


        if nx.has_path(graph, fromNode, toNode) == False:
            return None, None, "-->" + absence1 + "和" + absence2 + "之間不存在有效連結"


        # Find last connected row from inputColSrc to the block's colSrc
        pathNodes = nx.shortest_path(graph, fromNode, toNode)

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

            rows = postFile.loc[postFile[postCol] == preVal]
            if rows.empty:
                return None, None, "連結中斷，檔案" + str(postNode) + "中的'" \
                    + str(postCol) + "'欄位找不到此值: " + str(preVal)
            curRow = rows.iloc[0]

        # Get the final value
        blkColSrc = self.colSource[2]

        #isStr = pd.api.types.is_string_dtype(curRow[blkColSrc])
        #print("DB isStr = {0}".format(isStr))
        #if isStr:
        #    data = str(curRow.at[blkColSrc])
        #else:
        data = curRow.at[blkColSrc]

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


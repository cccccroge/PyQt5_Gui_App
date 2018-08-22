from PyQt5 import QtWidgets
import block

class dataFilterBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("資料篩選")

        self.settingData["dataType"] = ""
        self.settingData["filterCond"] = ""

        self.setAcceptDrops(True)

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog content
        # filtered data type
        groupBoxDataType = QtWidgets.QGroupBox(self.tr("篩選項目"))
        groupBoxDataTypeLayout = QtWidgets.QVBoxLayout()
        groupBoxDataType.setLayout(groupBoxDataTypeLayout)
        self.settingLayout.addWidget(groupBoxDataType)

        radioBtnStr = QtWidgets.QRadioButton(self.tr("文字"))
        radioBtnNum = QtWidgets.QRadioButton(self.tr("數字"))
        radioBtnDate = QtWidgets.QRadioButton(self.tr("日期"))

        self.radioBtnGroup = QtWidgets.QButtonGroup()
        self.radioBtnGroup.addButton(radioBtnStr, 0)
        self.radioBtnGroup.addButton(radioBtnNum, 1)
        self.radioBtnGroup.addButton(radioBtnDate, 2)

        groupBoxDataTypeLayout.addWidget(radioBtnStr)
        groupBoxDataTypeLayout.addWidget(radioBtnNum)
        groupBoxDataTypeLayout.addWidget(radioBtnDate)

        # condition string
        groupBoxCond = QtWidgets.QGroupBox(self.tr("條件式"))
        groupBoxCondLayout = QtWidgets.QVBoxLayout()
        groupBoxCond.setLayout(groupBoxCondLayout)
        self.settingLayout.addWidget(groupBoxCond)

        self.lineEditCond = QtWidgets.QLineEdit()
        groupBoxCondLayout.addWidget(self.lineEditCond)
        

    def generateOut(self, input, inputColSrc, graph):
        # Invalid input
        if type(input) != pd.core.frame.DataFrame \
            and type(input) != pd.core.series.Series:
                print("輸出時某'資料'方塊之輸入無效")
                return None, None
        
        fromNode = inputColSrc[0:2]
        toNode = self.colSource[0:2]
        # Failed to relate
        if (fromNode not in graph) or (toNode not in graph):
            print("輸出時出現檔案關聯失敗：某一資料表不曾被連結")
            return None, None

        if nx.has_path(graph, fromNode, toNode) == False:
            print("輸出時出現檔案關聯失敗：兩個資料表間不存在有效連結")
            return None, None


        # Same file: no need to traverse the graph
        if fromNode == toNode:
            data = self.filter(input)
            return data, self.colSource

        # Find second last connected row, and use filter setting to get rows or row
        if type(input) == pd.core.frame.DataFrame:
            input = input.iloc[0]
        curRow = input

        pathNodes = nx.shortest_path(graph, fromNode, toNode)
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
                print("輸出時，檔案關聯期間連結錯誤：兩個資料表的共同欄位值不同步")
                return None, None
            # don't cut in last round
            if i != len(pathNodes) - 2:
                curRow = rows.iloc[0]

        # Get the final rows/row
        data = self.filter(curRow)
        return data, self.colSource


    def filter(self, input):
        # Identify the data type
        type = self.settingData["dataType"]
        if type == "str":
            self.filter_str(input)
        elif  type == "num":
            self.filter_num(input)
        elif type == "date":
            self.filter_date(input)

    def filter_str(self, input):
        condStrs = self.settingData["filterCond"].split()
        # No filter
        if len(condStrs) <= 1:
            return input

        first = condStrs[0]
        second = condStrs[1]
        col = self.colSource[2]

        out = None
        if first == "=":
            out = input.loc[input[col] == second]

        return out


    def filter_num(self, input):
        condStrs = self.settingData["filterCond"].split()
        # No filter
        if len(condStrs) <= 1:
            return input

        first = condStrs[0]
        second = condStrs[1]
        col = self.colSource[2]

        out = None
        if first == "=":
            out = input.loc[input[col] == second]

        return out

    def filter_date(self, input):
        condStrs = self.settingData["filterCond"].split()
        # No filter
        if len(condStrs) <= 1:
            return input

        first = condStrs[0]
        second = condStrs[1]
        col = self.colSource[2]

        out = None
        if second == "latest":
            out = input.loc[input[col] == max(input[col])]
        elif second == "earliest":
            out = input.loc[input[col] == min(input[col])]
        else:
            second = int(second)
            if first == "=":
                out = input.loc[input[col] == second]
            elif first == "<":
                out = input.loc[input[col] < second]
            elif first == "<=":
                out = input.loc[input[col] <= second]
            elif first == ">":
                out = input.loc[input[col] > second]
            elif first == ">=":
                out = input.loc[input[col] >= second]

        return out


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
     

    ####################
    #      Slots
    ####################

    # Popup setting window for dataFilter block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__idOld = self.radioBtnGroup.checkedId()
        self.__textOld = self.lineEditCond.text()

        self.settingDialog.exec()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        id = self.radioBtnGroup.checkedId()
        if id == -1:
            self.settingData["dataType"] = ""
        elif id == 0:
            self.settingData["dataType"] = "str"
        elif id == 1:
            self.settingData["dataType"] = "num"
        elif id == 2:
            self.settingData["dataType"] = "date"

        self.settingData["filterCond"] = ""
        if id == -1:
            print("settingData becomes: ")
            print(self.settingData)
            return
        self.settingData["filterCond"] = self.lineEditCond.text()

        print("settingData becomes: ")
        print(self.settingData)

    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        if self.__idOld != -1:
            btn = self.radioBtnGroup.button(self.__idOld)
            btn.setChecked(True)

        self.lineEditCond.setText(self.__textOld)



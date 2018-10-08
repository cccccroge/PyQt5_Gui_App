from PyQt5 import QtWidgets
import pandas as pd
import numpy as np
import networkx as nx
import block
import dropEdit
import datetime
import glob

class dataFilterBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("資料篩選")

        self.settingData["satisfyCol"] = ()
        self.settingData["satisfyCond"] = ""
        self.settingData["dataType"] = ""
        self.settingData["filterCond"] = ""
        self.settingData["origChecked"] = False

        self.setAcceptDrops(True)

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog content
        # satisfied condition
        groupBoxSatisfy = QtWidgets.QGroupBox(self.tr("滿足條件"))
        groupBoxSatisfyLayout = QtWidgets.QVBoxLayout()
        groupBoxSatisfy.setLayout(groupBoxSatisfyLayout)
        self.settingLayout.addWidget(groupBoxSatisfy)

        self.lineEditSatisfy = dropEdit.dropEdit(False)
        groupBoxSatisfyLayout.addWidget(self.lineEditSatisfy)

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

        # use original checkbox
        self.origCheckbox = QtWidgets.QCheckBox(self.tr("使用原檔案"))
        groupBoxDataTypeLayout.addWidget(self.origCheckbox)
        groupBoxDataTypeLayout.addSpacing(10)

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
        # Use original file checked: don't care graph and input
        if self.settingData["origChecked"] == True:
            origFile = self.parent.srcFiles[self.colSource[0:2]]

            # check should be filtered
            satCond = self.settingData["satisfyCond"]
            if satCond != "":
                satCol = self.settingData["satisfyCol"][2]
                satDf = origFile.loc[origFile[satCol] == satCond]
                if satDf.empty:
                    return input, inputColSrc, ""

            data, msg = self.filter(origFile)
            return data, self.colSource, msg

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
        
        fromNode = inputColSrc[0:2]
        toNode = self.colSource[0:2]

        # Same file: don't care graph
        if fromNode == toNode:
            # check should be filtered
            satCond = self.settingData["satisfyCond"]
            if satCond != "":
                satCol = self.settingData["satisfyCol"][2]
                satDf = input.loc[input[satCol] == satCond]
                if satDf.empty:
                    return input, inputColSrc, ""

            data, msg = self.filter(input)
            return data, self.colSource, msg

        # Failed to relate
        absence1 = str(fromNode) if (fromNode not in graph) else ""
        absence2 = str(tomNode) if (toNode not in graph) else ""
        if absence1 == "" and absence2 != "":
            return None, None, "-->" + absence2 + "不曾被連結"
        if absence1 != "" and absence2 == "":
            return None, None, "-->" + absence1 + "不曾被連結"
        if absence1 != "" and absence2 != "":
            return None, None, "-->" + absence1 + "和" + absence2 + "皆不曾被連結"


        if nx.has_path(graph, fromNode, toNode) == False:
            return None, None, "-->" + absence1 + "和" + absence2 + "之間不存在有效連結"

        ## Find second last connected row, and use filter setting to get rows or row
        #if type(input) == pd.core.frame.DataFrame:
        #    input = input.iloc[0]
        curRow = input  # curRow is df

        pathNodes = nx.shortest_path(graph, fromNode, toNode)
        for i in range(len(pathNodes) - 1):
            # each relationship find another row
            preNode = pathNodes[i]
            postNode = pathNodes[i + 1]
            pre2postPath = graph[preNode][postNode]["common"]
            print("pre2postPath = {0}".format(pre2postPath))
            preCol = pre2postPath[0]
            postCol = pre2postPath[1]
            
            preVal = curRow[preCol] # preVal is Series
            print("preVal series is {0}".format(preVal))
            #preVal = preVal.iloc[:,0]
            li = preVal.tolist()

            postFile = self.parent.srcFiles[postNode]
            rows = postFile[postFile[postCol].isin(li)]
            print("rows is: {0}".format(rows))

            if rows.empty:
                return None, None, "-->連結中斷，檔案" + str(postNode) + "中的'" \
                    + str(postCol) + "'欄位找不到此值: " + str(preVal)

            # don't cut in last round
            if i != len(pathNodes) - 2:
                curRow = rows.iloc[0]
            else:
                curRow = rows

        # Get the final rows/row
        # check should be filtered
        satCond = self.settingData["satisfyCond"]
        if satCond != "":
            satCol = self.settingData["satisfyCol"][2]
            satDf = curRow.loc[curRow[satCol] == satCond]
            if satDf.empty:
                return input, inputColSrc, ""

        data, msg = self.filter(curRow)
        return data, self.colSource, msg


    def filter(self, input):
        # Identify the data type
        type = self.settingData["dataType"]
        if type == "":
            return input, ""
        if type == "str":
            return self.filter_str(input)
        elif type == "num":
            return self.filter_num(input)
        elif type == "date":
            return self.filter_date(input)


    def filter_str(self, input):
        condStrs = self.settingData["filterCond"].split()
        # No filter
        if len(condStrs) <= 1:
            return None, "-->條件式非法: 沒有空格分開"

        first = condStrs[0]
        second = condStrs[1]
        col = self.colSource[2]

        # modify second if needed
        if second == "special":
            name = self.settingData["satisfyCond"]
            # find planyr (has to exist)
            planyrId = -1
            grid = self.field.gridLayout
            for i in range(grid.rowCount() - 1):
                hbox = grid.itemAtPosition(i, 0)
                rowName = hbox.itemAt(1).widget().text()
                if rowName == "申請計畫年度":
                    planyrId = i
                    break
            
            planyr = self.parent.tempData[str(planyrId)]
            second = glob.get_special_years(name, planyr)
            if second is None:
                second = ""

        out = None
        if first == "=":
            #if second.find("<") != -1 and second.find(">") != -1:   # use another val
            #    row = second[second.find("<") + 1:second.find(">")]
            #    second = str(self.parent.tempData[str(int(row)-1)])
            #    print("second str after = is: {0}".format(second))
            orPos = second.find("OR")
            if orPos == -1:
                string = self.formulaToString(second)
                out = input.loc[input[col] == string]
            else:   # assume only one OR
                second1 = second[0:orPos]
                second2 = second[orPos + 2:]
                string1 = self.formulaToString(second1)
                string2 = self.formulaToString(second2)
                stringList = [string1, string2]
                out = input[input[col].isin(stringList)]
        elif first == "!=":
            out = input.loc[input[col] != second]
        elif first == "contains":
            string = str(self.formulaToString(second))
            containList = []
            # Get all vals into list
            while True:
                orPos = string.find("OR")
                if orPos == -1:
                    containList.append(string)
                    break
                else:
                    e = string[:orPos]
                    containList.append(e)
                    string = string[orPos + 2:]

            pattern = "|".join(containList)
            out = input[input[col].str.contains(pattern) == True]

            print("out = {0}".format(out))
        else:
            return None, "-->條件式非法: 出現未知的運算子"

        if out.empty:
            return None, "-->找不到符合此條件式之項目: " \
                + str(self.colSource) + " " + self.settingData["filterCond"]
        else:
            return out, ""


    def filter_num(self, input):
        condStrs = self.settingData["filterCond"].split()
        # No filter
        if len(condStrs) <= 1:
            return None, "-->條件式非法: 沒有空格分開"

        first = condStrs[0]
        second = condStrs[1]
        col = self.colSource[2]

        out = None

        if first == "=":
            if second == "max:":
                out = input.loc[input[col] == max(input[col])]
            elif second == "min":
                out = input.loc[input[col] == min(input[col])]
            elif second.isdigit():
                second = int(second)
                out = input.loc[input[col] == second]
            else:
                return None, "-->條件式非法: 第二項不是非負整數"

        else:
            if not second.isdigit():
                return None, "-->條件式非法: 第二項不是非負整數"
            
            second = int(second)
            if first == "=":
                out = input.loc[input[col] == second]   # assume data is string
            elif first == "<":
                out = input.loc[input[col] < second]
            elif first == "<=":
                out = input.loc[input[col] <= second]
            elif first == ">":
                out = input.loc[input[col] > second]
            elif first == ">=":
                out = input.loc[input[col] >= second]
            else:
                return None, "-->條件式非法: 出現未知的運算子"

        if out.empty:
            return None, "-->找不到符合此條件式之項目: " \
                + str(self.colSource) + " " + self.settingData["filterCond"]
        else:
            return out, ""


    def filter_date(self, input):
        condStrs = self.settingData["filterCond"].split()
        # No filter
        if len(condStrs) <= 1:
            return None, "-->條件式非法: 沒有空格分開"

        first = condStrs[0]
        second = condStrs[1]
        col = self.colSource[2]

        out = None

        if first == "=":
            if second == "latest":
                out = input.loc[input[col] == max(input[col])]
            elif second == "earliest":
                out = input.loc[input[col] == min(input[col])]
            elif second.isdigit():
                second = int(second)
                out = input.loc[input[col] == second]
            else:
                return None, "-->條件式非法: 第二項不是合法日期格式"

        else:
            # Translate TODAY to date string
            if second == "TODAY":
                second = datetime.datetime.now().strftime("%Y%m%d")

            if not second.isdigit():
                return None, "-->條件式非法: 第二項不是合法日期格式"
            second = str(second)    # src date must be string

            if first == "<":
                out = input.loc[input[col] < second]
            elif first == "<=":
                out = input.loc[input[col] <= second]
            elif first == ">":
                out = input.loc[input[col] > second]
            elif first == ">=":
                out = input.loc[input[col] >= second]
            else:
                return None, "-->條件式非法: 出現未知的運算子"

        if out.empty:
            return None, "-->找不到符合此條件式之項目: " \
                + str(self.colSource) + " " + self.settingData["filterCond"]
        else:
            return out, ""


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
        self.__satColOld = self.lineEditSatisfy.colSource
        self.__satCondOld = self.lineEditSatisfy.text()
        self.__idOld = self.radioBtnGroup.checkedId()
        self.__textOld = self.lineEditCond.text()
        self.__checkedOld = self.origCheckbox.isChecked()

        self.settingDialog.show()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        self.settingData["satisfyCol"] = self.lineEditSatisfy.colSource
        self.settingData["satisfyCond"] = self.lineEditSatisfy.text()

        id = self.radioBtnGroup.checkedId()
        if id == -1:
            self.settingData["dataType"] = ""
        elif id == 0:
            self.settingData["dataType"] = "str"
        elif id == 1:
            self.settingData["dataType"] = "num"
        elif id == 2:
            self.settingData["dataType"] = "date"

        self.settingData["origChecked"] = self.origCheckbox.isChecked()

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
        self.lineEditSatisfy.colSource = self.__satColOld
        self.lineEditSatisfy.setText(self.__satCondOld)

        if self.__idOld != -1:
            btn = self.radioBtnGroup.button(self.__idOld)
            btn.setChecked(True)

        self.lineEditCond.setText(self.__textOld)
        self.origCheckbox.setChecked(self.__checkedOld)
    

    ####################
    # Helper functions
    ####################

    def formulaToString(self, formula):
        curFormula = formula
        if curFormula == "":
            return curFormula

        while True:
            leftSqBrc = curFormula.find("<")

            # All temp variables are replaced
            if leftSqBrc == -1:
                break

            rightSqBrc = curFormula.find(">")

            # Get actual data and replace it
            row = int(curFormula[leftSqBrc + 1:rightSqBrc])
            data = self.parent.tempData[str(row-1)]
            if data is None:
                data = ""

            toReplaced = "<" + str(row) + ">"
            print("toReplaced = {0}, data = {1}".format(toReplaced, data))
            curFormula = curFormula.replace(toReplaced, "'" + str(data) + "'")
            print("curFormula becomes: {0}".format(curFormula))
            print("result: {0}".format(eval(curFormula)))

        if curFormula.isdigit():
            return float(curFormula)
        else:
            needToAdd = True if (curFormula[0] != "'" and curFormula[0] != "\"") else False
            if needToAdd:
                toEval = "\"" + curFormula.strip() + "\""
            else:
                toEval = curFormula.strip()

            return eval(toEval)



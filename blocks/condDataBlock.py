from PyQt5 import QtWidgets, QtCore
import block, dropEdit
import datetime
import pandas as pd
import numpy as np

class condDataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("條件資料")

        self.settingData["dataType"] = ""
        self.settingData["mapRules"] = []

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog conetent
        # data type
        groupBoxDatatype = QtWidgets.QGroupBox(self.tr("類型"))
        groupBoxDatatypeLayout = QtWidgets.QVBoxLayout()
        groupBoxDatatype.setLayout(groupBoxDatatypeLayout)
        self.settingLayout.addWidget(groupBoxDatatype)
        
        radioBtnExist = QtWidgets.QRadioButton(self.tr("是否存在"))
        radioBtnVal = QtWidgets.QRadioButton(self.tr("值"))
        radioBtnUseform = QtWidgets.QRadioButton(self.tr("使用對應表"))

        self.radioBtnGroup = QtWidgets.QButtonGroup()
        self.radioBtnGroup.addButton(radioBtnExist, 0)
        self.radioBtnGroup.addButton(radioBtnVal, 1)
        self.radioBtnGroup.addButton(radioBtnUseform, 2)
        self.radioBtnGroup.buttonClicked[int].connect(self.on_radioBtnGroup_buttonClicked)

        groupBoxDatatypeLayout.addWidget(radioBtnExist)
        groupBoxDatatypeLayout.addWidget(radioBtnVal)
        groupBoxDatatypeLayout.addWidget(radioBtnUseform)

        # map values for existence
        self.groupBoxMaprules = QtWidgets.QGroupBox(self.tr("對應值"))
        self.groupBoxMaprulesLayout = QtWidgets.QGridLayout()
        self.groupBoxMaprules.setLayout(self.groupBoxMaprulesLayout)
        self.groupBoxMaprules.hide()
        self.settingLayout.addWidget(self.groupBoxMaprules)

        yesLabel = QtWidgets.QLabel(self.tr("是"))
        mapIcon1 = QtWidgets.QLabel(self.tr("=>"))
        self.lineEditYes = QtWidgets.QLineEdit()
        noLabel = QtWidgets.QLabel(self.tr("否"))
        mapIcon2 = QtWidgets.QLabel(self.tr("=>"))
        self.lineEditNo = QtWidgets.QLineEdit()

        self.groupBoxMaprulesLayout.addWidget(yesLabel, 0, 0)
        self.groupBoxMaprulesLayout.addWidget(mapIcon1, 0, 1)
        self.groupBoxMaprulesLayout.addWidget(self.lineEditYes, 0, 2)
        self.groupBoxMaprulesLayout.addWidget(noLabel, 1, 0)
        self.groupBoxMaprulesLayout.addWidget(mapIcon2, 1, 1)
        self.groupBoxMaprulesLayout.addWidget(self.lineEditNo, 1, 2)

        # map values for value
        self.groupBoxMaprules2 = QtWidgets.QGroupBox(self.tr("對應值"))
        self.groupBoxMaprulesLayout2 = QtWidgets.QGridLayout()
        self.groupBoxMaprules2.setLayout(self.groupBoxMaprulesLayout2)
        self.groupBoxMaprules2.hide()
        self.settingLayout.addWidget(self.groupBoxMaprules2)

        for i in range(10):
            lineEditfrom = QtWidgets.QLineEdit()
            mapIcon = QtWidgets.QLabel(self.tr("=>"))
            lineEditTo = QtWidgets.QLineEdit()

            self.groupBoxMaprulesLayout2.addWidget(lineEditfrom, i, 0)
            self.groupBoxMaprulesLayout2.addWidget(mapIcon, i, 1)
            self.groupBoxMaprulesLayout2.addWidget(lineEditTo, i, 2)

        # map setting for useform
        self.groupBoxMapUseform = QtWidgets.QGroupBox(self.tr("對應設定"))
        self.groupBoxMapUseformLayout = QtWidgets.QGridLayout()
        self.groupBoxMapUseform.setLayout(self.groupBoxMapUseformLayout)
        self.groupBoxMapUseform.hide()
        self.settingLayout.addWidget(self.groupBoxMapUseform)

        limitLabel = QtWidgets.QLabel(self.tr("使用表格/欄位限制"))
        self.limitEdit = dropEdit.dropEdit(False)
        mapLabel = QtWidgets.QLabel(self.tr("對應"))
        self.fromEdit = dropEdit.dropEdit(True)
        self.fromEdit.setReadOnly(True)
        mapIcon = QtWidgets.QLabel(self.tr("=>"))
        self.toEdit = dropEdit.dropEdit(True)
        self.toEdit.setReadOnly(True)

        self.groupBoxMapUseformLayout.addWidget(limitLabel, 0, 0)
        self.groupBoxMapUseformLayout.addWidget(self.limitEdit, 0, 1)
        self.groupBoxMapUseformLayout.addWidget(mapLabel, 1, 0)
        self.groupBoxMapUseformLayout.addWidget(self.fromEdit, 1, 1)
        self.groupBoxMapUseformLayout.addWidget(mapIcon, 1, 2)
        self.groupBoxMapUseformLayout.addWidget(self.toEdit, 1, 3)

        # stretch at the end
        self.settingLayout.addStretch()


    def generateOut(self, input):
        out = None
        ruleList = self.settingData["mapRules"]

        # No rules
        if (ruleList is None) or len(ruleList) == 0:
            return None, "-->對應規則為空"

        # if is existence, must has out
        if self.settingData["dataType"] == "existence":
            if input is None:
                out = self.formulaToVal(ruleList[1][1])
            else:
                out = self.formulaToVal(ruleList[0][1])

            return out, ""

        # No data
        if input is None:
            return None, "-->使用值/表格值來對應但資料為空"


        isFind = False
        if self.settingData["dataType"] == "value":
            # Find match
            for tup in ruleList:
                fromVal = tup[0]
                # is a single data
                if len(fromVal.split()) == 1:   
                    if input == tup[0]:
                        isFind = True
                        out = self.formulaToVal(tup[1])
                        break
                # is a condition
                else:
                    if self.numSatisfy(input, fromVal) == True:
                        isFind = True
                        out = self.formulaToVal(tup[1])
                        break

        elif self.settingData["dataType"] == "useform": # hack a bit bcz failed to get orig type in excel
            for tup in ruleList:
                if input == int(tup[0]):
                    isFind = True
                    out = tup[1]
                    break
        
        if isFind == False:
            for tup in ruleList:
                if tup[0] == "others":
                    out = self.formulaToVal(tup[1])
                    break

        if out is None:
            return out, "-->該項目找不到對應規則"

        return out, ""
                

    ####################
    #      Slots
    ####################

    # Popup setting window for condData block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__idOld = self.radioBtnGroup.checkedId()

        self.__textsOld = []
        for row in range(self.groupBoxMaprulesLayout.rowCount()):
            t1 = self.groupBoxMaprulesLayout.itemAtPosition(row, 0).widget().text()
            t2 = self.groupBoxMaprulesLayout.itemAtPosition(row, 2).widget().text()
            self.__textsOld.append((t1, t2))

        self.__textsOld2 = []
        for row in range(self.groupBoxMaprulesLayout2.rowCount()):
            t1 = self.groupBoxMaprulesLayout2.itemAtPosition(row, 0).widget().text()
            t2 = self.groupBoxMaprulesLayout2.itemAtPosition(row, 2).widget().text()
            self.__textsOld2.append((t1, t2))

        self.__textLimitOld = self.limitEdit.text()

        self.settingDialog.show()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        id = self.radioBtnGroup.checkedId()
        if id == -1:
            self.settingData["dataType"] = ""
        elif id == 0:
            self.settingData["dataType"] = "existence"
        elif id == 1:
            self.settingData["dataType"] = "value"
        elif id == 2:
            self.settingData["dataType"] = "useform"


        self.settingData["mapRules"] = []
        targetLayout = None
        if id == -1:
            print("settingData becomes: ")
            print(self.settingData)
            return
        elif id == 0:
            targetLayout = self.groupBoxMaprulesLayout
        elif id == 1:
            targetLayout = self.groupBoxMaprulesLayout2
        elif id == 2:
            self.settingData["mapRules"] = self.getMapRulesUseform()
            print("settingData becomes: ")
            print(self.settingData)
            return

        for row in range(targetLayout.rowCount()):
            t1 = targetLayout.itemAtPosition(row, 0).widget().text()
            t2 = targetLayout.itemAtPosition(row, 2).widget().text()
            if t1 == "" and t2 == "":
                continue

            self.settingData["mapRules"].append((t1, t2))

        print("settingData becomes: ")
        print(self.settingData)

    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        if self.__idOld != -1:
            btn = self.radioBtnGroup.button(self.__idOld)
            btn.setChecked(True)
            self.radioBtnGroup.buttonClicked[int].emit(self.__idOld)

        for row in range(self.groupBoxMaprulesLayout.rowCount()):
            self.groupBoxMaprulesLayout.itemAtPosition(row, 0).widget() \
                .setText(self.__textsOld[row][0])
            self.groupBoxMaprulesLayout.itemAtPosition(row, 2).widget() \
                .setText(self.__textsOld[row][1])

        for row in range(self.groupBoxMaprulesLayout2.rowCount()):
            self.groupBoxMaprulesLayout2.itemAtPosition(row, 0).widget() \
                .setText(self.__textsOld2[row][0])
            self.groupBoxMaprulesLayout2.itemAtPosition(row, 2).widget() \
                .setText(self.__textsOld2[row][1])

        self.limitEdit.setText(self.__textLimitOld)


    def on_radioBtnGroup_buttonClicked(self, id):
        if id == 0:
            self.groupBoxMaprules2.hide()
            self.groupBoxMapUseform.hide()
            self.groupBoxMaprules.show()
        elif id == 1:
            self.groupBoxMaprules.hide()
            self.groupBoxMapUseform.hide()
            self.groupBoxMaprules2.show()
        elif id == 2:
            self.groupBoxMaprules.hide()
            self.groupBoxMaprules2.hide()
            self.groupBoxMapUseform.show()


    ####################
    # Helper functions
    ####################

    def getMapRulesUseform(self):
        colSrc = self.limitEdit.colSource
        if colSrc is None:
            print("沒有對應檔案")
            return []

        limitFileKey = colSrc[0:2]
        limitName = colSrc[2]
        df = self.parent.srcFiles[limitFileKey]

        df2 = None
        # Cut if has limit
        if self.limitEdit.text() != "":
            limitVal = self.limitEdit.text()    # limitVal should be int
            df2 = df.loc[df[limitName] == int(limitVal)]    # df[] will lost dtype
        else:
            df2 = df


        # Get rule tuples
        fromCol = self.fromEdit.text()
        toCol = self.toEdit.text()

        if fromCol == "" or toCol == "":
            print("對應設定無效")
            return []

        ruleTuples = []
        for index, row in df2.iterrows():
            tup = (row[fromCol], row[toCol])
            ruleTuples.append(tup)

        return ruleTuples


    def numSatisfy(self, num, cond):
        num = str(float(num))
        return eval(num + cond)


    def formulaToVal(self, formula):
        curFormula = formula

        while True:
            leftSqBrc = curFormula.find("<")

            # All temp variables are replaced
            if leftSqBrc == -1:
                break

            rightSqBrc = curFormula.find(">")

            # Get actual data and replace it
            row = curFormula[leftSqBrc + 1:rightSqBrc]
            data = self.parent.tempData[str(int(row)-1)]

            # is multiData, convert to list
            if type(data) == pd.core.frame.DataFrame:  
                data.astype("float64")
                data = data.fillna(0)
                data = data.iloc[:,0]   # convert to series
                data = data.tolist()
                data = sum(data)    # hack a bit

                toReplaced = "sum(<" + row + ">)"
                curFormula = curFormula.replace(toReplaced, str(data))
                print("is DataFrame, curFormula becomes: {0}".format(curFormula))
            elif type(data) == pd.core.frame.Series:
                data.astype("float64")
                data.fillna(0)
                data = data.tolist()    # how about NaN?
                data = sum(data)

                toReplaced = "sum(<" + row + ">)"
                curFormula = curFormula.replace(toReplaced, str(data))
                print("is Series, curFormula becomes: {0}".format(curFormula))

            # normal number
            else:
                if data is None:
                    data = ""
                else:
                    if data.isdigit():
                        data = float(data)
                    else:
                        data = "'" + data + "'"

                toReplaced = "<" + row + ">"
                curFormula = curFormula.replace(toReplaced, str(data))
                print("either DataFrame or Series, curFormula becomes: {0}".format(curFormula))

        while True:
            todayPos = curFormula.find("TODAY")
            if todayPos == -1:
                break

            todayStr = datetime.datetime.now().strftime("%Y%m%d")
            curFormula = curFormula.replace("TODAY", str(todayStr))

        if (type(curFormula).__module__ == np.__name__) or curFormula.isdigit():
            print("digit")
            curFormula = float(curFormula)
        else:
            print("not digit")
            curFormula = "'" + curFormula + "'"

        return eval(str(curFormula))



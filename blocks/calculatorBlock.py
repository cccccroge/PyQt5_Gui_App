from PyQt5 import QtWidgets
import pandas as pd
import math
import block

class calculatorBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("計算")

        self.enableSettingDialog()

        self.settingData["formula"] = ""
        self.settingData["useExcelFormula"] = False
        self.settingData["approxMethod"] = ""
        self.settingData["approxDigit"] = 0

        self.setAcceptDrops(True)

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog content
        # formula group
        groupboxFormula = QtWidgets.QGroupBox(self.tr("運算式"))
        groupboxFormulaLayout = QtWidgets.QVBoxLayout()
        groupboxFormula.setLayout(groupboxFormulaLayout)
        self.settingLayout.addWidget(groupboxFormula)

        self.useExcelCheckbox = QtWidgets.QCheckBox(self.tr("使用Excel公式"))
        groupboxFormulaLayout.addWidget(self.useExcelCheckbox)
        self.formulaEdit = QtWidgets.QLineEdit()
        groupboxFormulaLayout.addWidget(self.formulaEdit)

        # approx settings group
        groupboxApprox = QtWidgets.QGroupBox(self.tr("近似設定"))
        groupboxApproxLayout = QtWidgets.QHBoxLayout()
        groupboxApprox.setLayout(groupboxApproxLayout)
        self.settingLayout.addWidget(groupboxApprox)

        self.approxMethodCombo = QtWidgets.QComboBox()
        self.approxMethodCombo.addItem(self.tr("四捨五入"))
        self.approxMethodCombo.addItem(self.tr("無條件進位"))
        self.approxMethodCombo.addItem(self.tr("無條件捨去"))

        toTheLabel = QtWidgets.QLabel(self.tr("至第"))

        self.approxDigitSpin = QtWidgets.QSpinBox()
        self.approxDigitSpin.setRange(-20, 20)
        self.approxDigitSpin.setValue(1) # 1 means approx to in ones

        digitLabel = QtWidgets.QLabel(self.tr("位"))

        groupboxApproxLayout.addWidget(self.approxMethodCombo)
        groupboxApproxLayout.addWidget(toTheLabel)
        groupboxApproxLayout.addWidget(self.approxDigitSpin)
        groupboxApproxLayout.addWidget(digitLabel)


    def generateOut(self, valRow): # need to know round index, in case use excel formula
        result = 0

        if self.settingData["useExcelFormula"] == True:
            result = self.formulaToExcelForm(self.settingData["formula"], valRow)
            return result, ""


        result = self.formulaToVal(self.settingData["formula"])
        # Consider approx
        m = self.settingData["approxMethod"]
        d = self.settingData["approxDigit"]

        if m == "round":
            quotient = round(result / pow(10, d))
            result = quotient * pow(10, d)
        elif m == "ceil":
            quotient = math.ceil(result / pow(10, d))
            result = quotient * pow(10, d)
        elif m == "floor":
            quotient = math.floor(result / pow(10, d))
            result = quotient * pow(10, d)

        return result, ""
     

    ####################
    #      Slots
    ####################

    # Popup setting window for dataFilter block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__formulaOld = self.formulaEdit.text()
        self.__useExcelOld = self.useExcelCheckbox.isChecked()
        self.__methodIndexOld = self.approxMethodCombo.currentIndex()
        self.__digitNumOld = self.approxDigitSpin.value()

        self.settingDialog.exec()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        self.settingData["formula"] = self.formulaEdit.text()
        self.settingData["useExcelFormula"] = self.useExcelCheckbox.isChecked()

        id = self.approxMethodCombo.currentIndex()
        if id == -1:
            self.settingData["approxMethod"] = ""
        elif id == 0:
            self.settingData["approxMethod"] = "round"
        elif id == 1:
            self.settingData["approxMethod"] = "ceil"
        elif id == 2:
            self.settingData["approxMethod"] = "floor"
        
        self.settingData["approxDigit"] = self.approxDigitSpin.value()

        print("settingData becomes: ")
        print(self.settingData)


    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        self.formulaEdit.setText(self.__formulaOld)
        self.useExcelCheckbox.setChecked(self.__useExcelOld)

        if self.__methodIndexOld != -1:
            self.approxMethodCombo.setCurrentIndex(self.__methodIndexOld)

        self.approxDigitSpin.setValue(self.__digitNumOld)


    ####################
    # Helper functions
    ####################

    def formulaToVal(self, formula):
        equal = formula.find("=")
        if equal != -1:
            curFormula = formula[equal + 1:]
        #curFormula = (curFormula.split())[1]   # user don't need to enter '='

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
                    return 0
                else:
                    data = float(self.parent.tempData[row]) # assume the others are float

                toReplaced = "<" + row + ">"
                curFormula = curFormula.replace(toReplaced, str(data))
                print("either DataFrame or Series, curFormula becomes: {0}".format(curFormula))

        return eval(curFormula)

    def formulaToExcelForm(self, formula, valRow):
        curFormula = "= " + formula

        while True:
            print("curFormula = {0}".format(curFormula))
            leftSqBrc = curFormula.find("<")

            # All temp variables are replaced
            if leftSqBrc == -1:
                break

            rightSqBrc = curFormula.find(">")

            # Calculate the number iterm of excel index
            row = curFormula[leftSqBrc + 1:rightSqBrc]
            first, second = divmod(int(row), 26)    # excel's 1 is A, not 0
            print("first = {0}, second = {1}".format(first, second))

            index = ""
            if first == 0:
                index = self.numToAlph(second)
            else:
                if first == 1 and second == 0:
                    index = "Z"
                elif first != 1 and second == 0:
                    index = self.numToAlph(first - 1) + "Z"
                else:
                    index = self.numToAlph(first) + self.numToAlph(second)
            index += str(valRow + 1)   # becomes cell position
            print("toString should be {0}".format(index))
            # Replace it
            toReplaced = "<" + row + ">"
            curFormula = curFormula.replace(toReplaced, index)
            print("After replacement: {0}".format(curFormula))

        return curFormula


    def numToAlph(self, num):
        if num > 26 or num < 1:
            return None

        mapList = ["A", "A", "B", "C", "D", "E", "F", "G", "H", \
            "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", \
            "S", "T", "U", "V", "W", "X", "Y", "Z"]

        return mapList[num]
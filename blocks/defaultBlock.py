import block
from PyQt5 import QtWidgets
import datetime

class defaultBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("預設值")

        self.enableSettingDialog()

        self.settingData["useNum"] = False
        self.settingData["val"] = ""

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog content
        # val group
        groupboxVal = QtWidgets.QGroupBox(self.tr("預設值"))
        groupboxValLayout = QtWidgets.QVBoxLayout()
        groupboxVal.setLayout(groupboxValLayout)
        self.settingLayout.addWidget(groupboxVal)

        self.useNumber = QtWidgets.QCheckBox(self.tr("數字"))
        groupboxValLayout.addWidget(self.useNumber)
        self.valEdit = QtWidgets.QLineEdit()
        groupboxValLayout.addWidget(self.valEdit)

    def generateOut(self):
        out = None

        isNum = self.settingData["useNum"]
        if isNum:
            out = float(self.formulaToVal(self.settingData["val"]))
        else:
            out = self.formulaToVal(self.settingData["val"])

        return out, ""


    ####################
    #      Slots
    ####################

    # Popup setting window for default block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__useNum = self.useNumber.isChecked()
        self.__valOld = self.valEdit.text()

        self.settingDialog.exec()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        self.settingData["useNum"] = self.useNumber.isChecked()
        self.settingData["val"] = self.valEdit.text()

        print("settingData becomes: ")
        print(self.settingData)


    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        self.valEdit.setText(self.__valOld)
        self.useNumber.setChecked(self.__useNum)


    ####################
    # Helper functions
    ####################

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

        if curFormula.isdigit():
            print("digit")
            curFormula = float(curFormula)
        else:
            print("not digit")
            curFormula = "'" + curFormula + "'"

        return eval(str(curFormula))

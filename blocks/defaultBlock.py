import block
from PyQt5 import QtWidgets

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
            out = float(self.settingData["val"])
        else:
            out = self.settingData["val"]

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



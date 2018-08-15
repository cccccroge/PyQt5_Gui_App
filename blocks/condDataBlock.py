from PyQt5 import QtWidgets
import block

class condDataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.settingData["dataType"] = ""
        self.settingData["mapRules"] = []

        self.enableSettingDialog()

        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog conetent
        groupBoxDatatype = QtWidgets.QGroupBox(self.tr("類型"))
        groupBoxDatatypeLayout = QtWidgets.QVBoxLayout()
        groupBoxDatatype.setLayout(groupBoxDatatypeLayout)
        self.settingLayout.addWidget(groupBoxDatatype)
        
        radioBtnExist = QtWidgets.QRadioButton(self.tr("是否存在"))
        radioBtnVal = QtWidgets.QRadioButton(self.tr("值"))

        self.radioBtnGroup = QtWidgets.QButtonGroup()
        self.radioBtnGroup.addButton(radioBtnExist, 0)
        self.radioBtnGroup.addButton(radioBtnVal, 1)

        groupBoxDatatypeLayout.addWidget(radioBtnExist)
        groupBoxDatatypeLayout.addWidget(radioBtnVal)
        


    ####################
    #      Slots
    ####################

    # Popup setting window for condData block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__idOld = self.radioBtnGroup.checkedId()
        self.settingDialog.exec()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        id = self.radioBtnGroup.checkedId()
        if id == -1:
            self.settingData["dataType"] = ""
        elif id == 0:
            self.settingData["dataType"] = "existence"
        elif id == 1:
            self.settingData["dataType"] = "value"


    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        oldId = self.__idOld
        newId = self.radioBtnGroup.checkedId()

        if oldId == -1:
            if newId != -1:
                btn = self.radioBtnGroup.button(newId)
                self.radioBtnGroup.setExclusive(False)
                btn.setChecked(False)
                self.radioBtnGroup.setExclusive(True)
        else:
            btn = self.radioBtnGroup.button(oldId)
            btn.setChecked(True)



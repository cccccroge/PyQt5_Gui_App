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
        # data type
        groupBoxDatatype = QtWidgets.QGroupBox(self.tr("類型"))
        groupBoxDatatypeLayout = QtWidgets.QVBoxLayout()
        groupBoxDatatype.setLayout(groupBoxDatatypeLayout)
        self.settingLayout.addWidget(groupBoxDatatype)
        
        radioBtnExist = QtWidgets.QRadioButton(self.tr("是否存在"))
        radioBtnVal = QtWidgets.QRadioButton(self.tr("值"))

        self.radioBtnGroup = QtWidgets.QButtonGroup()
        self.radioBtnGroup.addButton(radioBtnExist, 0)
        self.radioBtnGroup.addButton(radioBtnVal, 1)
        self.radioBtnGroup.buttonClicked[int].connect(self.on_radioBtnGroup_buttonClicked)

        groupBoxDatatypeLayout.addWidget(radioBtnExist)
        groupBoxDatatypeLayout.addWidget(radioBtnVal)

        # map values for existence
        self.groupBoxMaprules = QtWidgets.QGroupBox(self.tr("對應值"))
        groupBoxMaprulesLayout = QtWidgets.QGridLayout()
        self.groupBoxMaprules.setLayout(groupBoxMaprulesLayout)

        yesLabel = QtWidgets.QLabel(self.tr("是"))
        mapIcon1 = QtWidgets.QLabel(self.tr("=>"))
        self.lineEditYes = QtWidgets.QLineEdit()
        noLabel = QtWidgets.QLabel(self.tr("否"))
        mapIcon2 = QtWidgets.QLabel(self.tr("=>"))
        self.lineEditNo = QtWidgets.QLineEdit()

        groupBoxMaprulesLayout.addWidget(yesLabel, 0, 0)
        groupBoxMaprulesLayout.addWidget(mapIcon1, 0, 1)
        groupBoxMaprulesLayout.addWidget(self.lineEditYes, 0, 2)
        groupBoxMaprulesLayout.addWidget(noLabel, 1, 0)
        groupBoxMaprulesLayout.addWidget(mapIcon2, 1, 1)
        groupBoxMaprulesLayout.addWidget(self.lineEditNo, 1, 2)

        # map values for value
        self.groupBoxMaprules2 = QtWidgets.QGroupBox(self.tr("對應值"))
        groupBoxMaprulesLayout2 = QtWidgets.QGridLayout()
        self.groupBoxMaprules2.setLayout(groupBoxMaprulesLayout2)
        #self.settingLayout.addWidget(groupBoxMaprules2)

        for i in range(5):
            lineEditfrom = QtWidgets.QLineEdit()
            mapIcon = QtWidgets.QLabel(self.tr("=>"))
            lineEditTo = QtWidgets.QLineEdit()

            groupBoxMaprulesLayout2.addWidget(lineEditfrom, i, 0)
            groupBoxMaprulesLayout2.addWidget(mapIcon, i, 1)
            groupBoxMaprulesLayout2.addWidget(lineEditTo, i, 2)


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


    def on_radioBtnGroup_buttonClicked(self, id):
        ret = self.settingLayout.findChild(QtWidgets.QGroupBox, "groupBoxMaprules")
        if self.settingLayout.widget() != None:
            self.settingLayout.s

        if id == 0:
            self.settingLayout.addWidget(self.groupBoxMaprules)
        elif id == 1:
            self.settingLayout.addWidget(self.groupBoxMaprules2)


from PyQt5 import QtWidgets, QtCore
import block

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

        self.radioBtnGroup = QtWidgets.QButtonGroup()
        self.radioBtnGroup.addButton(radioBtnExist, 0)
        self.radioBtnGroup.addButton(radioBtnVal, 1)
        self.radioBtnGroup.buttonClicked[int].connect(self.on_radioBtnGroup_buttonClicked)

        groupBoxDatatypeLayout.addWidget(radioBtnExist)
        groupBoxDatatypeLayout.addWidget(radioBtnVal)

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

        for i in range(5):
            lineEditfrom = QtWidgets.QLineEdit()
            mapIcon = QtWidgets.QLabel(self.tr("=>"))
            lineEditTo = QtWidgets.QLineEdit()

            self.groupBoxMaprulesLayout2.addWidget(lineEditfrom, i, 0)
            self.groupBoxMaprulesLayout2.addWidget(mapIcon, i, 1)
            self.groupBoxMaprulesLayout2.addWidget(lineEditTo, i, 2)

        # stretch at the end
        self.settingLayout.addStretch()


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


    def on_radioBtnGroup_buttonClicked(self, id):
        if id == 0:
            if not self.groupBoxMaprules2.isHidden():
                self.groupBoxMaprules2.hide()
            self.groupBoxMaprules.show()
        elif id == 1:
            if not self.groupBoxMaprules.isHidden():
                self.groupBoxMaprules.hide()
            self.groupBoxMaprules2.show()


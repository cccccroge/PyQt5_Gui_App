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



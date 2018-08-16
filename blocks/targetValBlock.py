from PyQt5 import QtWidgets
import block

class targetValBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("目標值")

        self.setAcceptDrops(True)

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog content
        groupBoxVals = QtWidgets.QGroupBox(self.tr("指定值"))
        groupBoxValsLayout = QtWidgets.QVBoxLayout()
        groupBoxVals.setLayout(groupBoxValsLayout)
        self.settingLayout.addWidget(groupBoxVals)

        self.textEdit = QtWidgets.QTextEdit()
        groupBoxValsLayout.addWidget(self.textEdit)


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

    # Popup setting window for condData block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__textOld = self.textEdit.toPlainText()

        self.settingDialog.exec()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        self.settingData["targetVals"] = []

        vals = self.textEdit.toPlainText().split()
        for val in vals:
            self.settingData["targetVals"].append(val)

        print("settingData becomes: ")
        print(self.settingData)

    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        self.textEdit.setPlainText(self.__textOld)
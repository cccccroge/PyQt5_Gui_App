from PyQt5 import QtWidgets, QtCore
import block

class iterateBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("迭代取值")

        self.settingData["???"] # TODO

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog content
        # selected list
        groupBoxIterRow = QtWidgets.QGroupBox(self.tr("迭代項目"))
        groupBoxIterRowLayout = QtWidgets.QVBoxLayout()
        groupBoxIterRow.setLayout(groupBoxIterRowLayout)
        self.settingLayout.addWidget(groupBoxIterRow)

        self.selectedRowList = QtWidgets.QListWidget()
        grid = self.field.gridLayout    # init list
        for i in range(0, grid.rowCount() - 1):
            hboxLayout = grid.itemAtPosition(i, 0)
            id = hboxLayout.itemAt(0).widget().text()
            name = hboxLayout.itemAt(1).widget().text()

            item = QtWidgets.QListWidgetItem()
            item.setText("<" + id + "> " + name)
            item.setFlags(item.flags() or QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.selectedRowList.addItem(item)
        self.selectedRowList.itemChanged.connect(self.on_selectedRowList_itemChanged)
        groupBoxIterRowLayout.addWidget(self.selectedRowList)

        # take value combo
        groupBoxTakeVal = QtWidgets.QGroupBox(self.tr("取值"))
        groupBoxTakeValLayout = QtWidgets.QVBoxLayout()
        groupBoxTakeVal.setLayout(groupBoxTakeValLayout)
        self.settingLayout.addWidget(groupBoxTakeVal)

        self.takeValCombo = QtWidgets.QComboBox()
        groupBoxTakeValLayout.addWidget(self.takeValCombo)



    ####################
    #      Slots
    ####################

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__checkedList = []
        for i in range(0, self.selectedRowList.count()):
            item = self.selectedRowList.item(i)
            checked = (item.checkState() == QtCore.Qt.Checked)
            if checked:
                self.__checkedList.append(i)

        self.__textList = []
        for i in range(0, self.takeValCombo.count()):
            text = self.takeValCombo.itemText(i)
            self.__textList.append(text)
        self.__selectedIndex = self.takeValCombo.currentIndex()

        self.settingDialog.exec()

    def on_selectedRowList_itemChanged(self, item):
        targetText = item.text()
        curCheckState = item.checkState()

        # Insert at appropriate position
        if curCheckState == QtCore.Qt.Checked:
            leftBck = targetText.find("<")
            rightBck = targetText.find(">")
            insertedId = int(targetText[leftBck + 1:rightBck])

            pos = -1
            for i in range(0, self.takeValCombo.count()):
                text = self.takeValCombo.itemText(i)
                leftBck = text.find("<")
                rightBck = text.find(">")
                id = int(text[leftBck + 1:rightBck])
                if insertedId > id:
                    continue
                else:
                    pos = i
                    break
            if pos == -1:
                pos = self.takeValCombo.count()

            self.takeValCombo.insertItem(pos, targetText)

        # Find and remove
        else:
            pos = -1
            for i in range(0, self.takeValCombo.count()):
                text = self.takeValCombo.itemText(i)
                if targetText == text:
                    pos = i
                else:
                    continue

            self.takeValCombo.removeItem(pos)

    def on_settingDialog_rejected(self):
        for i in range(0, self.selectedRowList.count()):
            item = self.selectedRowList.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)
        for idx in self.__checkedList:
            item = self.selectedRowList.item(idx)
            item.setCheckState(QtCore.Qt.Checked)

        self.takeValCombo.clear()
        for text in self.__textList:
            self.takeValCombo.addItem(text)
        self.takeValCombo.setCurrentIndex(self.__selectedIndex)

    def on_settingDialog_accepted(self):
        pass    # TODO: save to self.settingData["???"]...
                



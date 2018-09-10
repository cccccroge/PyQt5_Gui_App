from PyQt5 import QtWidgets
import block
import pandas as pd
import numpy as np
import networkx as nx

from glob import msgDuration

class multiDataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("多重資料")
        self.colSource = []
        self.setAcceptDrops(True)

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)
        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # List all element in colSource
        groupBoxShowCol = QtWidgets.QGroupBox(self.tr("顯示欄位"))
        groupBoxShowColLayout = QtWidgets.QVBoxLayout()
        groupBoxShowCol.setLayout(groupBoxShowColLayout)
        self.settingLayout.addWidget(groupBoxShowCol)

        self.showColList = QtWidgets.QListWidget()
        self.showColList.itemDoubleClicked.connect(self.on_showColList_itemDoubleClicked)
        groupBoxShowColLayout.addWidget(self.showColList)


    def generateOut(self, input, inputColSrc, graph):
        # No input
        if input is None:
            return None, None, "-->資料輸入為空"

        # Invalid input
        if type(input) != pd.core.frame.DataFrame \
            and type(input) != pd.core.series.Series:
                return None, None, "-->資料不是'表格'或'列'"
        
        # No data
        if input.empty:
            print("in dataBlock: input is {0}".format(input))
            return None, None, "-->資料表(/列)為空表(/列)"

        # Get the final value
        selectedColsList = self.colSource   # should identify if cols exist in file
        data = input[selectedColsList]

        return data, self.colSource, ""


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

        # Check if already in list
        for e in self.colSource:
            if colName == e:
                self.parent.statusBar().showMessage(
                    "該欄位已存在於多重資料方塊的列表中", msgDuration)   # this message is overwritten
                return

        # Store col to block
        self.colSource.append(colName)

        # Show item in listWidget
        new = QtWidgets.QListWidgetItem()
        new.setText(colName)
        self.showColList.addItem(new)

        print("drop source: {0}".format(self.colSource))
        event.acceptProposedAction()


    ####################
    #      Slots
    ####################

    # Popup setting window for multiData block

    def on_settingBtn_pressed(self):
        # Store old values in case user need to discard changes
        self.__listOld = self.colSource.copy()

        self.settingDialog.show()


    # Confirm setting window: store value to settingData

    def on_settingDialog_accepted(self):
        print("colSource becomes: {0}".format(self.colSource))


    # Cancel setting window: reset to old values

    def on_settingDialog_rejected(self):
        self.colSource = self.__listOld

        self.showColList.clear()
        for col in self.colSource:
            item = QtWidgets.QListWidgetItem()
            item.setText(col)
            self.showColList.addItem(item)

        print("colSource becomes: {0}".format(self.colSource))


    # Remove item when user double click on it

    def on_showColList_itemDoubleClicked(self, item):
        text = item.text()
        print("item to be removed is {0}".format(item))
        print("text to be removed is {0}".format(text))
        self.colSource.remove(text)

        index = self.showColList.row(item)
        ret = self.showColList.takeItem(index)
        del ret

from PyQt5 import QtWidgets, QtGui

import sys
sys.path.append("./blocks")
import dataBlock

class blockMenu(QtWidgets.QMenu):
    def __init__(self, parent, field, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.field = field

        dataAction = self.addAction(self.tr("資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(1))

        dataAction = self.addAction(self.tr("條件資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(2))

        dataAction = self.addAction(self.tr("資料篩選"))
        dataAction.triggered.connect(lambda: self.buildingBlock(3))

        dataAction = self.addAction(self.tr("數量"))
        dataAction.triggered.connect(lambda: self.buildingBlock(4))

        dataAction = self.addAction(self.tr("計算"))
        dataAction.triggered.connect(lambda: self.buildingBlock(5))


    ####################
    #      Slots
    ####################

    # Build corresponding type of block

    def buildingBlock(self, id):
        if id == 1:
            # This block temporarily belongs to field
            # It'll be actually put into gridLayout (bodyWidget) when user press leftbutton
            blk = dataBlock.dataBlock(self.parent, self.field)
            blk.setParent(self.field)

            # Set to correct position (cursor at its center) at beginning
            blkCord = blk.mapFromGlobal(QtGui.QCursor.pos())
            parentCord = blk.mapToParent(blkCord)
            blk.move(parentCord - blk.offset)

            blk.show()
        

from PyQt5 import QtWidgets, QtGui

import sys
sys.path.append("./blocks")
import targetValBlock, dataBlock, multiDataBlock, condDataBlock
import dataFilterBlock, numberBlock, calculatorBlock, useAnotherBlock, defaultBlock
import styleBlock, iterateBlock

class blockMenu(QtWidgets.QMenu):
    def __init__(self, parent, field, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.field = field

        dataAction = self.addAction(self.tr("目標值"))
        dataAction.triggered.connect(lambda: self.buildingBlock(0))

        dataAction = self.addAction(self.tr("資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(1))

        dataAction = self.addAction(self.tr("多重資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(2))

        dataAction = self.addAction(self.tr("條件資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(3))

        dataAction = self.addAction(self.tr("資料篩選"))
        dataAction.triggered.connect(lambda: self.buildingBlock(4))

        dataAction = self.addAction(self.tr("數量"))
        dataAction.triggered.connect(lambda: self.buildingBlock(5))

        dataAction = self.addAction(self.tr("計算"))
        dataAction.triggered.connect(lambda: self.buildingBlock(6))

        dataAction = self.addAction(self.tr("取其它"))
        dataAction.triggered.connect(lambda: self.buildingBlock(7))

        dataAction = self.addAction(self.tr("預設值"))
        dataAction.triggered.connect(lambda: self.buildingBlock(8))

        dataAction = self.addAction(self.tr("樣式"))
        dataAction.triggered.connect(lambda: self.buildingBlock(9))

        dataAction = self.addAction(self.tr("迭代取值"))
        dataAction.triggered.connect(lambda: self.buildingBlock(10))


    ####################
    #      Slots
    ####################

    # Build corresponding type of block

    def buildingBlock(self, id):
        # This block temporarily belongs to field
        # It'll be actually put into gridLayout (bodyWidget) when user press leftbutton
        blk = None

        if id == 0:
            blk = targetValBlock.targetValBlock(self.parent, self.field)
        elif id == 1:
            blk = dataBlock.dataBlock(self.parent, self.field)
        elif id == 2:
            blk = multiDataBlock.multiDataBlock(self.parent, self.field)
        elif id == 3:
            blk = condDataBlock.condDataBlock(self.parent, self.field)
        elif id == 4:
            blk = dataFilterBlock.dataFilterBlock(self.parent, self.field)
        elif id == 5:
            blk = numberBlock.numberBlock(self.parent, self.field)
        elif id == 6:
            blk = calculatorBlock.calculatorBlock(self.parent, self.field)
        elif id == 7:
            blk = useAnotherBlock.useAnotherBlock(self.parent, self.field)
        elif id == 8:
            blk = defaultBlock.defaultBlock(self.parent, self.field)
        elif id == 9:
            blk = styleBlock.styleBlock(self.parent, self.field)
        elif id == 10:
            blk = iterateBlock.iterateBlock(self.parent, self.field)
        else:
            return

        blk.setParent(self.field)

        # Set to correct position (cursor at its center) at beginning
        blkCord = blk.mapFromGlobal(QtGui.QCursor.pos())
        parentCord = blk.mapToParent(blkCord)
        blk.move(parentCord - blk.offset)

        blk.show()
        

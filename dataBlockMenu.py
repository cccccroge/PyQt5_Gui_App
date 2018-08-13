from PyQt5 import QtWidgets, QtGui

import dataBlock

class dataBlockMenu(QtWidgets.QMenu):
    def __init__(self, parent, field, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.field = field

        dataAction = self.addAction(self.tr("資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(1))


    def buildingBlock(self, id):
        if id == 1:
            # This block is a temporary object
            # It'll be actually constructed (put into gridLayout)
            # when user press leftbutton
            blk = dataBlock.dataBlock(self.parent, self.field)
            blk.setParent(self.field)

            # Set this temp object to correct position
            blkCord = blk.mapFromGlobal(QtGui.QCursor.pos())
            parentCord = blk.mapToParent(blkCord)
            blk.move(parentCord - blk.offset)

            blk.show()
        

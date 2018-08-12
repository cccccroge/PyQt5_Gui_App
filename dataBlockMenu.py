from PyQt5 import QtWidgets, QtGui

import dataBlock

class dataBlockMenu(QtWidgets.QMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent

        dataAction = self.addAction(self.tr("資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(1))


    def buildingBlock(self, id):
        if id == 1:
            blk = dataBlock.dataBlock()
            blk.setParent(self.parent)
            self.parent.activeBlock = blk
            #self.parent.layout().addWidget(blk)
            self.parent.setMouseTracking(True)
            blk.show()
        

from PyQt5 import QtWidgets

class dataBlockMenu(QtWidgets.QMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Options
        dataAction = self.addAction(self.tr("資料"))
        dataAction.triggered.connect(lambda: self.buildingBlock(1))


    def buildingBlock(self, id):
        if id == 1:
            print("正在建造data block..")

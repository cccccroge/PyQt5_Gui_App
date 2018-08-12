from PyQt5 import QtWidgets

class dataBlock(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Widget elements
        hboxLayout = QtWidgets.QHBoxLayout()
        self.setLayout(hboxLayout)

        self.nameEdit = QtWidgets.QLineEdit()
        self.nameEdit.setPlaceholderText(self.tr("方塊"))
        self.settingBtn = QtWidgets.QPushButton()
        self.settingBtn.setText(self.tr("設定"))

        hboxLayout.addWidget(self.nameEdit)
        hboxLayout.addWidget(self.settingBtn)


    

from PyQt5 import QtWidgets, QtCore

import list

class properties(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        vboxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(vboxLayout)
        self.parent = parent

        # Head
        headWidget = QtWidgets.QWidget()
        p1 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p1.setVerticalStretch(2)
        headWidget.setSizePolicy(p1)

        gridLayout = QtWidgets.QGridLayout()
        comboBox = QtWidgets.QComboBox()
        comboBox.currentIndexChanged[str].connect(self.on_comboBox_currentIndexChanged)
        parent.comboBox = comboBox
        labelImage = QtWidgets.QLabel()
        labelImage.setText("放大鏡")
        lineEdit = QtWidgets.QLineEdit()
        lineEdit.setPlaceholderText(self.tr("搜尋欄位名稱"))
        gridLayout.addWidget(comboBox, 0, 0, 1, 2)
        gridLayout.addWidget(labelImage, 1, 0)
        gridLayout.addWidget(lineEdit, 1, 1)
        headWidget.setLayout(gridLayout)

        # List
        listWidget = list.list(parent)
        p2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p2.setVerticalStretch(12)
        listWidget.setSizePolicy(p2)
        

        # Button
        connectButton = QtWidgets.QPushButton()
        connectButton.setText(self.tr("建立聯結"))
        p3 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p3.setVerticalStretch(2)
        connectButton.setSizePolicy(p3)


        vboxLayout.addWidget(headWidget)
        vboxLayout.addWidget(listWidget)
        vboxLayout.addWidget(connectButton)

    # When item changed, show names of selected file
    def on_comboBox_currentIndexChanged(self, text):
        self.parent.list.showFile(text)


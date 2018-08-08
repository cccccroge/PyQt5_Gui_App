from PyQt5 import QtWidgets, QtCore

import list
import connectButton

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
        comboBox.addItem(self.tr("已連結"))
        comboBox.currentIndexChanged[str].connect(self.on_comboBox_currentIndexChanged)
        parent.comboBox = comboBox
        labelImage = QtWidgets.QLabel()
        labelImage.setText("放大鏡")
        lineEdit = QtWidgets.QLineEdit()
        self.lineEdit = lineEdit
        lineEdit.setPlaceholderText(self.tr("搜尋欄位名稱"))
        lineEdit.textEdited.connect(self.on_lineEdit_textEdited)
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
        button = connectButton.connectButton(parent)
        p3 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p3.setVerticalStretch(2)
        button.setSizePolicy(p3)

        vboxLayout.addWidget(headWidget)
        vboxLayout.addWidget(listWidget)
        vboxLayout.addWidget(button)



    ####################
    #      Slots
    ####################

    # When item changed, show names of selected file
    # Re-search on the new names

    def on_comboBox_currentIndexChanged(self, filename):
        self.parent.list.showFile(filename)
        self.parent.list.showSearch(self.lineEdit.text())

        
    # When text changed, show the search result

    def on_lineEdit_textEdited(self, searchText):
        self.parent.list.showSearch(searchText)

    




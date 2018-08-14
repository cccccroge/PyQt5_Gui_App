from PyQt5 import QtWidgets, QtCore, QtGui

import dataBlockMenu
from glob import msgDuration, fieldRowHeight

class field(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent

        vboxLayout1 = QtWidgets.QVBoxLayout()
        self.setLayout(vboxLayout1)

        # Head
        headWidget = QtWidgets.QWidget()
        p1 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p1.setVerticalStretch(2)
        headWidget.setSizePolicy(p1)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, 
                         QtGui.QColor(200, 200, 200, 255))
        headWidget.setAutoFillBackground(True)
        headWidget.setPalette(palette)

        addBlkBtn = QtWidgets.QPushButton()
        addBlkBtn.setText("選擇方塊")
        addBlkBtn.setFixedSize(QtCore.QSize(100, 50))
        popupMenu = dataBlockMenu.dataBlockMenu(self.parent, self)
        addBlkBtn.setMenu(popupMenu)

        previewButton = QtWidgets.QPushButton()
        previewButton.setText("預覽")
        previewButton.setFixedSize(QtCore.QSize(50, 25))
        previewButton.pressed.connect(parent.actions["viewExportedExcel"].trigger)
        exportButton = QtWidgets.QPushButton()
        exportButton.setText("輸出")
        exportButton.setFixedSize(QtCore.QSize(50, 25))
        exportButton.pressed.connect(parent.actions["exportExcel"].trigger)
        hboxLayout1 = QtWidgets.QHBoxLayout()
        hboxLayout1.addWidget(previewButton)
        hboxLayout1.addWidget(exportButton)
        hboxLayout1.setAlignment(QtCore.Qt.AlignRight)

        hboxLayout2 = QtWidgets.QHBoxLayout()
        hboxLayout2.setContentsMargins(25, 5, 25, 5)
        hboxLayout2.addWidget(addBlkBtn)
        hboxLayout2.addLayout(hboxLayout1)
        headWidget.setLayout(hboxLayout2)

        # Body
        self.bodyWidget = QtWidgets.QWidget()
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.bodyWidget)
        self.scrollArea.setWidgetResizable(True)
        p2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p2.setVerticalStretch(14)
        self.scrollArea.setSizePolicy(p2)

        vboxLayout2 = QtWidgets.QVBoxLayout()
        vboxLayout2.setAlignment(QtCore.Qt.AlignLeft)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)
        self.gridLayout.setContentsMargins(25, 25, 25, 25)
        self.gridLayout.setVerticalSpacing(25)
        self.gridLayout.setHorizontalSpacing(0)
        vboxLayout2.addLayout(self.gridLayout)
        vboxLayout2.addSpacing(400)
        hboxLayout3 = QtWidgets.QHBoxLayout()
        hboxLayout3.addLayout(vboxLayout2)
        hboxLayout3.addSpacing(900)
        self.bodyWidget.setLayout(hboxLayout3)

        # default cols
        for i in range(5):    
            col = self.__create_default_col()
            self.gridLayout.addWidget(col, i, 0, QtCore.Qt.AlignLeft)

        # add col button
        addColBtn = QtWidgets.QPushButton()
        addColBtn.setText("+")
        addColBtn.setFixedSize(25, 25)
        addColBtn.pressed.connect(self.on_addColBtn_pressed)
        self.gridLayout.addWidget(addColBtn, self.gridLayout.rowCount(), 
                                  0, QtCore.Qt.AlignLeft)


        vboxLayout1.addWidget(headWidget)
        vboxLayout1.addWidget(self.scrollArea)


    ####################
    #      Slots
    ####################

    # Add a new column when pressed

    def on_addColBtn_pressed(self):
        lastRow = self.gridLayout.rowCount() - 1;
        addColBtn = self.gridLayout.itemAtPosition(lastRow, 0).widget()
        newCol = self.__create_default_col()
        
        #self.gridLayout.removeWidget(addColBtn)
        self.gridLayout.addWidget(newCol, lastRow, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addWidget(addColBtn, lastRow + 1, 0, QtCore.Qt.AlignLeft)

        self.parent.statusBar().showMessage("新增一個欄位", msgDuration)


    ####################
    #   Private funcs
    ####################

    def __create_default_col(self):
        le = QtWidgets.QLineEdit()
        le.setPlaceholderText(self.tr("欄位名稱"))
        le.setFixedSize(QtCore.QSize(125, fieldRowHeight))
        return le



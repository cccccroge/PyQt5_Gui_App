from PyQt5 import QtWidgets, QtCore, QtGui

import blockMenu, block
from globalUsed import msgDuration, fieldRowHeight

class field(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

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
        popupMenu = blockMenu.blockMenu(self.parent, self)
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

        self.vboxLayout2 = QtWidgets.QVBoxLayout()
        self.vboxLayout2.setAlignment(QtCore.Qt.AlignLeft)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setAlignment(QtCore.Qt.AlignTop)
        self.gridLayout.setContentsMargins(25, 25, 25, 25)
        self.gridLayout.setVerticalSpacing(25)
        self.gridLayout.setHorizontalSpacing(0)
        self.vboxLayout2.addLayout(self.gridLayout)
        self.vboxLayout2.addSpacing(400)
        hboxLayout3 = QtWidgets.QHBoxLayout()
        hboxLayout3.addLayout(self.vboxLayout2)
        hboxLayout3.addSpacing(900)
        self.bodyWidget.setLayout(hboxLayout3)

        # default cols
        for i in range(5):    
            rowLayout = self.__create_row_hBoxLayout(i + 1)
            self.gridLayout.addLayout(rowLayout, i, 0, QtCore.Qt.AlignLeft)

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
        rowLayout = self.__create_row_hBoxLayout(lastRow + 1)
        
        self.gridLayout.addLayout(rowLayout, lastRow, 0, QtCore.Qt.AlignLeft)
        self.gridLayout.addWidget(addColBtn, lastRow + 1, 0, QtCore.Qt.AlignLeft)

        self.parent.statusBar().showMessage("新增一個欄位", msgDuration)


    ####################
    #    Overloadeds
    ####################

    def mouseDoubleClickEvent(self, QMouseEvent):
        if QMouseEvent.button() != QtCore.Qt.LeftButton:
            return

        # transform block-cord to fieldBody-cord
        globPos = self.mapToGlobal(QMouseEvent.pos())
        fieldBodyPos = self.bodyWidget.mapFromGlobal(globPos)
        pos = fieldBodyPos

        # decide row to add
        startRow = self.__getGridRow(pos.y() - fieldRowHeight / 2, self.gridLayout)
        if type(startRow) == int:
            print("on row {0}".format(startRow))
            self.parent.statusBar().showMessage("該位置不能插入列", msgDuration)
            return

        # Insert new row
        startRow = int(startRow + 0.5)
        self.__insert_new_row(startRow)


    def mousePressEvent(self, QMouseEvent):
        pass


    ####################
    #   Private funcs
    ####################

    def __create_default_col(self):
        le = QtWidgets.QLineEdit()
        le.setPlaceholderText(self.tr("欄位名稱"))
        le.setFixedSize(QtCore.QSize(125, fieldRowHeight))
        return le


    def __create_row_hBoxLayout(self, id):
        col = self.__create_default_col()
        rowLayout = QtWidgets.QHBoxLayout()
        rowLayout.setContentsMargins(0, 0, 0, 0)
        rowLayout.setSpacing(0)

        idEdit = QtWidgets.QLineEdit()
        idEdit.setText(str(id))
        idEdit.setAlignment(QtCore.Qt.AlignCenter)
        idEdit.setFixedSize(25, fieldRowHeight)
        idEdit.setReadOnly(True)
        rowLayout.addWidget(idEdit, 0, QtCore.Qt.AlignLeft)
        rowLayout.addWidget(col, 0, QtCore.Qt.AlignLeft)
        #rowLayout.addStretch(-1)
        return rowLayout


    def __insert_new_row(self, start):
        print("now insert row at: {0}".format(start))

        grid = self.gridLayout
        # Store all rows after inserted row (included)
        store = []
        for i in range(start, grid.rowCount()):
            item = grid.itemAtPosition(i, 0)
            grid.removeItem(item)
            store.append(item)

        # Add new row
        rowLayout = self.__create_row_hBoxLayout(start + 1)
        grid.addLayout(rowLayout, start, 0, QtCore.Qt.AlignLeft)

        # Restore old rows
        for idx, item in enumerate(store):
            if type(item) == QtWidgets.QHBoxLayout:
                print("adding hbox...")
                # increment index
                idEdit = item.itemAt(0).widget()
                newId = int(idEdit.text()) + 1
                idEdit.setText(str(newId))
                grid.addLayout(item, start + 1 + idx, 0, QtCore.Qt.AlignLeft)
            else:
                print("adding non-hbox...")
                grid.addWidget(item.widget(), start + 1 + idx, 0, QtCore.Qt.AlignLeft)
            #grid.addItem(item, start + 1 + idx, 0, QtCore.Qt.AlignLeft)

        self.parent.statusBar().showMessage("新增一個欄位", msgDuration)


    def __getGridRow(self, y, gridLayout):
        l, topMargin, r, b = gridLayout.getContentsMargins()
        y_eff = y - topMargin

        # Not even get to first row
        if y_eff < 0:
            return -0.5

        # Estimate row position
        verSpace = gridLayout.verticalSpacing()
        unit = fieldRowHeight + verSpace
        row  = int(y_eff / unit)

        # Exceed last row (exclude the addBtn)
        if row > gridLayout.rowCount() - 2:
            return (gridLayout.rowCount() - 2 + 0.5)

        # Not on the exact row (on spaces)
        if y_eff > unit * (row + 1) - verSpace:
            return (row + 0.5)

        return row



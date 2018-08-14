from PyQt5 import QtWidgets, QtCore, QtGui
from glob import msgDuration, fieldRowHeight

class block(QtWidgets.QWidget):
    def __init__(self, parent, field, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.field = field
        self.setFixedSize(120, fieldRowHeight)
        self.putRow = None

        # Widget elements
        hboxLayout = QtWidgets.QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        hboxLayout.setSpacing(0)
        self.setLayout(hboxLayout)

        self.nameEdit = QtWidgets.QLineEdit()
        self.nameEdit.setFixedSize(100, fieldRowHeight)
        self.nameEdit.setAcceptDrops(False)
        self.nameEdit.setDisabled(True)
        self.settingBtn = QtWidgets.QPushButton()
        self.settingBtn.setText(self.tr("..."))
        self.settingBtn.setFixedSize(20, fieldRowHeight)

        hboxLayout.addWidget(self.nameEdit, 0, QtCore.Qt.AlignLeft)
        hboxLayout.addWidget(self.settingBtn, 0, QtCore.Qt.AlignLeft)

        # Transparent background
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, 
                         QtGui.QColor(0, 0, 0, 0))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Controls
        self.setMouseTracking(True)
        self.offset = QtCore.QPoint(self.width() / 2, self.height() / 2)

    def disableBtn(self):
        self.settingBtn.deleteLater()
        self.setFixedSize(100, fieldRowHeight)
        self.offset = QtCore.QPoint(self.width() / 2, self.height() / 2)


    ####################
    #    Overloadeds
    ####################

    # Make block's center move with cursor

    def mouseMoveEvent(self, QMouseEvent):
        pos = self.mapToParent(QMouseEvent.pos()) - self.offset
        self.move(pos)

        #self.putRow = self.__getGridRow(pos.y(), self.field.gridLayout)


    # Actions when mouse button press

    def mousePressEvent(self, QMouseEvent):
        # Right mouse button to cancel
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.deleteLater()
            self.parent.statusBar().showMessage("已取消建立方塊", msgDuration)

        # Left mouse button to confirm
        else:
            # transform block-cord to fieldBody-cord
            globPos = self.mapToGlobal(QMouseEvent.pos())
            fieldBodyPos = self.field.bodyWidget.mapFromGlobal(globPos)
            pos = fieldBodyPos - self.offset

            # decide position to put
            self.putRow = self.__getGridRow(pos.y(), self.field.gridLayout)
            if self.putRow is None:
                self.parent.statusBar().showMessage("該位置不能放置方塊", msgDuration)
                return

            hboxLayout = self.field.gridLayout.itemAtPosition(self.putRow, 0)
            #putCol = self.__getGridCol(self.putRow, self.field.gridLayout)

            # put a line and a block to that row's hboxLayout
            self.setMouseTracking(False)

            lineLabel = QtWidgets.QLabel()
            lineLabel.setText("──")
            lineLabel.setFixedHeight(fieldRowHeight)
            hboxLayout.addWidget(lineLabel, 0, QtCore.Qt.AlignLeft)
            hboxLayout.addWidget(self, 0, QtCore.Qt.AlignLeft)
            #self.field.gridLayout.addWidget(
            #    lineLabel, self.putRow, putCol, QtCore.Qt.AlignLeft)
            #self.field.gridLayout.addWidget(
            #    self, self.putRow, putCol + 1, QtCore.Qt.AlignLeft)
            self.nameEdit.setDisabled(False)

            self.parent.statusBar().showMessage("已成功建立方塊", msgDuration)


    ####################
    #   Private funcs
    ####################

    # Get row index to put

    def __getGridRow(self, y, gridLayout):
        l, topMargin, r, b = gridLayout.getContentsMargins()
        y_eff = y - topMargin

        # Not even get to first row
        if y_eff < 0:
            return None

        # Estimate row position
        verSpace = gridLayout.verticalSpacing()
        unit = fieldRowHeight + verSpace
        row  = int(y_eff / unit)

        # Exceed last row (exclude the addBtn)
        if row > gridLayout.rowCount() - 2:
            return None

        # Not on the exact row (on spaces)
        if y_eff > unit * (row + 1) - verSpace:
            return None

        return row


    ## Get col index to put

    #def __getGridCol(self, row, gridLayout):
    #    col = 0
    #    while True:
    #        item = gridLayout.itemAtPosition(row, col)
    #        if item is None:
    #            break;
    #        col += 1

    #    return col


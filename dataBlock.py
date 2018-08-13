from PyQt5 import QtWidgets, QtCore, QtGui
from glob import msgDuration

class dataBlock(QtWidgets.QWidget):
    def __init__(self, parent, field, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.field = field
        self.setFixedSize(140, 25)

        # Widget elements
        hboxLayout = QtWidgets.QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hboxLayout)

        self.nameEdit = QtWidgets.QLineEdit()
        self.nameEdit.setFixedSize(100, 25)
        self.nameEdit.setDisabled(True)
        self.settingBtn = QtWidgets.QPushButton()
        self.settingBtn.setText(self.tr("設定"))
        self.settingBtn.setFixedSize(40, 25)

        hboxLayout.addWidget(self.nameEdit)
        hboxLayout.addWidget(self.settingBtn)

        # Transparent background
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, 
                         QtGui.QColor(0, 0, 0, 0))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Controls
        self.setMouseTracking(True)
        self.offset = QtCore.QPoint(self.width() / 2, self.height() / 2)


    def mouseMoveEvent(self, QMouseEvent):
        pos = self.mapToParent(QMouseEvent.pos())
        self.move(pos - self.offset)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.deleteLater()
            self.parent.statusBar().showMessage("已取消建立方塊", msgDuration)
        else:
            self.setMouseTracking(False)
            #self.field.gridLayout.addWidget(self, 0, 1, QtCore.Qt.AlignLeft)
            self.nameEdit.setDisabled(False)
            self.parent.statusBar().showMessage("已成功建立方塊", msgDuration)


    

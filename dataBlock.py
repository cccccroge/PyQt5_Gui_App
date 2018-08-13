from PyQt5 import QtWidgets, QtCore, QtGui

class dataBlock(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setFixedSize(140, 100)

        # Widget elements
        hboxLayout = QtWidgets.QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hboxLayout)

        self.nameEdit = QtWidgets.QLineEdit()
        self.nameEdit.setFixedSize(100, 25)
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
        self.offset = QtCore.QPoint(self.width() / 2, self.height() / 2 + 30)
        self.installEventFilter(self)

    def mouseMoveEvent(self, QMouseEvent):
        pos = self.mapToParent(QMouseEvent.pos())
        self.move(pos - self.offset)

    def mousePressEvent(self, QMouseEvent):
        self.setMouseTracking(False)


        


    

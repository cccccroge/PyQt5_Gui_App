from PyQt5 import QtWidgets, QtCore, QtGui

import dataBlockMenu

class field(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.activeBlock = None
        self.setMouseTracking(False)

        vboxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(vboxLayout)

        # Body
        self.bodyWidget = QtWidgets.QWidget()
        p2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p2.setVerticalStretch(14)
        self.bodyWidget.setSizePolicy(p2)

        b1 = QtWidgets.QPushButton()
        b1.setText("隨意")
        b1.setFixedSize(QtCore.QSize(50, 25))

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setContentsMargins(25, 5, 25, 5)
        gridLayout.addWidget(b1, 0, 0, QtCore.Qt.AlignLeft)
        self.bodyWidget.setLayout(gridLayout)

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

        addButton = QtWidgets.QPushButton()
        addButton.setText("選擇方塊")
        addButton.setFixedSize(QtCore.QSize(100, 50))
        popupMenu = dataBlockMenu.dataBlockMenu(self)
        addButton.setMenu(popupMenu)

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
        hboxLayout2.addWidget(addButton)
        hboxLayout2.addLayout(hboxLayout1)
        headWidget.setLayout(hboxLayout2)


        vboxLayout.addWidget(headWidget)
        vboxLayout.addWidget(self.bodyWidget)
    

    def mouseMoveEvent(self, QMouseEvent):
        pos = QMouseEvent.pos()
        print(pos)
        #print("mouse in field is at {1}".format(pos))
        #self.activeBlock.move(pos)

    def mousePressEvent(self, QMouseEvent):
        self.setMouseTracking(False)
        self.activeBlock = None

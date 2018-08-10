from PyQt5 import QtWidgets, QtCore, QtGui

class field(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent

        vboxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(vboxLayout)

        # Head
        headWidget = QtWidgets.QWidget()
        p1 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p1.setVerticalStretch(2)
        headWidget.setSizePolicy(p1)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(200, 200, 200, 255))
        headWidget.setAutoFillBackground(True)
        headWidget.setPalette(palette)

        addButton = QtWidgets.QPushButton()
        addButton.setText("+")
        addButton.setFixedSize(QtCore.QSize(50, 50))

        #previewButton = QtWidgets.QPushButton()
        #previewButton.setText("預覽")
        #previewButton.setFixedSize(QtCore.QSize(50, 25))
        #exportButton = QtWidgets.QPushButton()
        #exportButton.setText("輸出")
        #exportButton.setFixedSize(QtCore.QSize(50, 25))
        buttonMenu = QtWidgets.QMenu()
        buttonMenu.addAction(self.parent.actions["viewExportedExcel"])
        buttonMenu.addAction(self.parent.actions["exportExcel"])
        hboxLayout1 = QtWidgets.QHBoxLayout()
        hboxLayout1.addWidget(buttonMenu)
        hboxLayout1.setAlignment(QtCore.Qt.AlignRight)

        hboxLayout2 = QtWidgets.QHBoxLayout()
        hboxLayout2.setContentsMargins(25, 5, 25, 5)
        hboxLayout2.addWidget(addButton)
        hboxLayout2.addLayout(hboxLayout1)
        headWidget.setLayout(hboxLayout2)

        # Body
        bodyWidget = QtWidgets.QWidget()
        p2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p2.setVerticalStretch(14)
        bodyWidget.setSizePolicy(p2)

        b1 = QtWidgets.QPushButton()
        b1.setText("隨意")
        b1.setFixedSize(QtCore.QSize(50, 25))
        l1 = QtWidgets.QLabel()
        l1.setText("HA")

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setContentsMargins(25, 5, 25, 5)
        gridLayout.addWidget(b1, 0, 0, QtCore.Qt.AlignLeft)
        bodyWidget.setLayout(gridLayout)


        vboxLayout.addWidget(headWidget)
        vboxLayout.addWidget(bodyWidget)



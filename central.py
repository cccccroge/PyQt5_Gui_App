import sys
from PyQt5 import QtWidgets, QtCore


class central(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # Central widget in mainWindow is a QTabwidget
        centralWidget = QtWidgets.QTabWidget()
        centralWidget.setTabsClosable(True)
        centralWidget.setMovable(True)
        centralWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        centralWidget.tabCloseRequested.connect(lambda: self.on_centralWidget_tabCloseRequested())
        self.connect(centralWidget, QtCore.pyqtSignal('tabCloseRequested(int)'),
            self, QtCore.pyqtSlot(on_centralWidget_tabCloseRequested))
        parent.setCentralWidget(centralWidget)

        # Main work space (loaded default)
        parent.mainWidget = QtWidgets.QSplitter()   # make field of mainWindow to access mainWidget in other places
        
        propertyWidget = QtWidgets.QWidget()
        propertyWidget.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Minimum)
        parent.mainWidget.addWidget(propertyWidget)

        fieldWidget = QtWidgets.QWidget()
        fieldWidget.sizePolicy().setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
        parent.mainWidget.addWidget(fieldWidget)

        parent.mainWidget.setStretchFactor(0, 1)
        parent.mainWidget.setStretchFactor(1, 5)

        centralWidget.addTab(parent.mainWidget, self.tr("主要工作面板"))


        # Test
        w = QtWidgets.QWidget()
        centralWidget.addTab(w, "2")

    def on_centralWidget_tabCloseRequested(self, index):
        print("YO")


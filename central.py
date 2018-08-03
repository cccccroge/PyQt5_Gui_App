import sys
from PyQt5 import QtWidgets, QtCore


class central(QtWidgets.QTabWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # Store mainWindow to use in slots
        self.mainWindow = parent

        # Set tabWidget properties
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabCloseRequested.connect(self.on_tabCloseRequested)
        parent.setCentralWidget(self)

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
        self.addTab(parent.mainWidget, self.tr("主要工作面板"))


        # Test
        w = QtWidgets.QWidget()
        self.addTab(w, "2")

    def on_tabCloseRequested(self, index):
        target = self.widget(index)

        # If is mainWidget, don't delete it
        if target == self.mainWindow.mainWidget:
            self.removeTab(index)
        else:
            target.deleteLater()
            self.removeTab(index)
        


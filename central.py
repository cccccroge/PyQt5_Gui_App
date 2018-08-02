import sys
from PyQt5 import QtWidgets

class central(QtWidgets.QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # Central widget in mainWindow is a QTabwidget
        centralWidget = QtWidgets.QTabWidget()
        centralWidget.setTabsClosable(True)
        centralWidget.setMovable(True)
        centralWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        parent.setCentralWidget(centralWidget)

        # Main work space (loaded default)
        parent.mainWidget = QtWidgets.QSplitter()
        propertyWidget = QtWidgets.QWidget()
        fieldWidget = QtWidgets.QWidget()
        parent.mainWidget.addWidget(propertyWidget)
        parent.mainWidget.addWidget(fieldWidget)

        centralWidget.addTab(parent.mainWidget, self.tr("主要工作面板"))


        # Test
        w = QtWidgets.QWidget()
        centralWidget.addTab(w, "2")


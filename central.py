import sys
from PyQt5 import QtWidgets, QtCore

import properties
import filed

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
        
        propertiesWidget = properties.properties(parent)
        parent.mainWidget.addWidget(propertiesWidget)

        fieldWidget = filed.filed(parent)
        parent.mainWidget.addWidget(fieldWidget)

        parent.mainWidget.setSizes([320, 1600])
        self.addTab(parent.mainWidget, self.tr("主要工作面板"))


        # Test
        #w = QtWidgets.QWidget()
        #self.addTab(w, "2")



    ####################
    #      Slots
    ####################

    def on_tabCloseRequested(self, index):
        target = self.widget(index)

        # If is mainWidget, don't delete it, just hide
        if target == self.mainWindow.mainWidget:
            self.removeTab(index)
        else:
            target.deleteLater()
            self.removeTab(index)
        


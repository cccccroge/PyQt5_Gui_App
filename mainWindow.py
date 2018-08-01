import sys
from PyQt5 import QtWidgets
import menuFile

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().menuBar().setNativeMenuBar(False)
        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.init_menu()

    def init_menu(self):
        # Using default menuBar of QMainWindow
        menu = menuFile.menuFile()
        self.menuBar().addMenu(menu)
        








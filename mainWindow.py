import sys
from PyQt5 import QtWidgets
import menu

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.init_ui()

    def init_ui(self):
        # Init menu
        menu.menu(self.menuBar())









import sys
from PyQt5 import QtWidgets
import mainWindow

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()

import sys
from PyQt5 import QtWidgets, QtCore
import mainWindow

#while True:
#    a = input()
#    a = str(a)
#    print(a.isnumeric())

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


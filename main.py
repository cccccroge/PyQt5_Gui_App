import sys
from PyQt5 import QtWidgets, QtCore
import mainWindow

#tempData = {}
#tempData['2'] = None
#print("val is {0}".format(float(tempData['2'])))

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


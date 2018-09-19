import sys
from PyQt5 import QtWidgets, QtCore
import mainWindow

#string2 = """ 'F301AA5172'[0:6]+'0000' """
#string = """ "'F301AA5172'[0:6]+'0000'" """
#print(eval(string))



app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


import sys
from PyQt5 import QtWidgets, QtCore
import mainWindow

#while True:
#    a = input()
#    a = str(a)
#    print(a.isnumeric())

#result = 6995931.77
#d = 3
#quotient = round(result / pow(10, d))
#print("quitient = {0}".format(quotient))
#result = quotient * pow(10, d)
#print("result = {0}".format(result))


app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


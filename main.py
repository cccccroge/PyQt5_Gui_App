import sys
from PyQt5 import QtWidgets, QtCore
import pandas as pd
import mainWindow
import math

#ll = [1.5, 3.77, 8.5231]
#print(math.fsum(ll))

#a = float(1.5)
#b = float(3.77)
#c = float(8.5231)
#print(a + b + c)



# enable unlimited col width of display forms
pd.set_option("display.max_colwidth", -1)

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


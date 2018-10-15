import sys
from PyQt5 import QtWidgets, QtCore
import pandas as pd
import mainWindow
import math


#num = "81106749"
#print("num is digit? {0}".format(num.isdigit()))
#print("num is int? {0}".format(isinstance(num, int)))
#print("num is float? {0}".format(isinstance(num, float)))
#print("num is float? {0}".format(isinstance(num, str)))

# enable unlimited col width of display forms
pd.set_option("display.max_colwidth", -1)

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()



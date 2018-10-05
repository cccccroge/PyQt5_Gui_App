import sys
from PyQt5 import QtWidgets, QtCore
import pandas as pd
import mainWindow
import math


# enable unlimited col width of display forms
pd.set_option("display.max_colwidth", -1)

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


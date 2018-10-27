import sys
from PyQt5 import QtWidgets, QtCore
from openpyxl.compat import unicode
import pandas as pd
import mainWindow
import math


# Test which is invalid character
#form = []
#form.append(["種"])
#form.append(["種"])
#form.append(["之"])
#form.append(["之"])


# Decode the same character
#print(ord("種"))
#print(ord("種"))
#if not isinstance("種", unicode):
#    print("first not unicode")
#if not isinstance("種", unicode):
#    print("first not unicode")


#df = pd.DataFrame(form)
#writer = pd.ExcelWriter("output.xlsx")
#df.to_excel(writer, "sheet1")
#writer.save()


# enable unlimited col width of display forms
pd.set_option("display.max_colwidth", -1)

app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()



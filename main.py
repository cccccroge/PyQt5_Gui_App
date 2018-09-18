import sys
from PyQt5 import QtWidgets, QtCore
import mainWindow

#import datetime
#curFormula = "TODAY"

#while True:
#    todayPos = curFormula.find("TODAY")
#    if todayPos == -1:
#        break

#    todayStr = datetime.datetime.now().strftime("%Y%m%d")
#    curFormula = curFormula.replace("TODAY", str(todayStr))

#if curFormula.isdigit():
#    print("digit")
#    curFormula = float(curFormula)
#else:
#    print("not digit")
#    curFormula = "'" + curFormula + "'"

#print(eval(str(curFormula)))



app = QtWidgets.QApplication(sys.argv)
w = mainWindow.mainWindow()
w.show()
app.exec()


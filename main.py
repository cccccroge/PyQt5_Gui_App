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

#import numpy as np
#from glob import make_red_font

#fileName = QtWidgets.QFileDialog.getSaveFileName(
#    None, "儲存檔案", ""
#    , "All Files (*);;Excel Files (*xlsx);;Excel 97-2003 Files(*xls)"
#    , "Excel Files (*xlsx)")

#lpos = fileName[1].rfind("(") + 2
#rpos = fileName[1].rfind(")")
#ext = "." + (fileName[1])[lpos:rpos]
#path = fileName[0]
#if path.find(ext) == -1:    # if user didn't type extension then add for them
#    path = path + ext
#writer = pd.ExcelWriter(path)

#np.random.seed(24)
#df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
#df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list('BCDE'))],
#               axis=1)
#ll = [(1, 2), (5, 3)]
#df = df.style.apply(make_red_font, axis=None, target=ll)
#df.to_excel(writer, "工作表1", header=False, index=False)

#writer.save()


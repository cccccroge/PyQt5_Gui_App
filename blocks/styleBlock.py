from PyQt5 import QtWidgets, QtCore, QtGui
from glob import msgDuration, fieldRowHeight
import numpy as np

import block

class styleBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("樣式")

        self.disableBtn()

    def generateOut(self, input, oriInput, oriColSrc):
        if (input is None) or (input == ""):
            return oriInput, oriColSrc, "-->前者資料為空"

        else:
            try:
                if np.isnan(input):
                    return oriInput, oriColSrc, "-->前者資料為無"
                else:
                    return input, None, ""
            except TypeError:
                return input, None, ""
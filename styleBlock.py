from PyQt5 import QtWidgets, QtCore, QtGui
from globalUsed import msgDuration, fieldRowHeight
import numpy as np

import block

class styleBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("樣式")

        self.disableBtn()

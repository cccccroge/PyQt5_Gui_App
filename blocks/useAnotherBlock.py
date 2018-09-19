import block
import numpy as np

class useAnotherBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("取其它")

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
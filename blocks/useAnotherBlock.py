import block

class useAnotherBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("取其它")

        self.disableBtn()


    def generateOut(self, input, oriInput, oriColSrc):
        if (input is None) or (input == ""):
            return oriInput, oriColSrc, "-->前者資料為無或空字串"
        else:
            return input, None, ""
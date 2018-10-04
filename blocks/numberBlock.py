import block

class numberBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("數量")
        self.disableBtn()

    def generateOut(self, input):
        out = None

        if input is None:
            out = 0
        else:
            print("type of input is:")
            print(type(input))
            out = len(input)  # input has to be dataframe

        return out
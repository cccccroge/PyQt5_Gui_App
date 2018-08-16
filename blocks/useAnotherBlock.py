import block

class useAnotherBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("取其它")

        self.disableBtn()

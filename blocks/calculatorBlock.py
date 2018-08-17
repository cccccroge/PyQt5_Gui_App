import block

class calculatorBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.nameEdit.setText("計算")

        self.enableSettingDialog()

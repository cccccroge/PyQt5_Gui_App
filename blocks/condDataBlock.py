from PyQt5 import QtWidgets
import block

class condDataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)


    ####################
    #      Slots
    ####################

    # Popup setting window for condData block
    def on_settingBtn_pressed(self):
        pass



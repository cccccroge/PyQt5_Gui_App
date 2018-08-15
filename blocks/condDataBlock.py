from PyQt5 import QtWidgets
import block

class condDataBlock(block.block):
    def __init__(self, parent, field, **kwargs):
        super().__init__(parent, field, **kwargs)

        self.enableSettingDialog()
        self.settingBtn.pressed.connect(self.on_settingBtn_pressed)

        self.settingDialog.accepted.connect(self.on_settingDialog_accepted)
        self.settingDialog.rejected.connect(self.on_settingDialog_rejected)

        # Dialog conetent
        


    ####################
    #      Slots
    ####################

    # Popup setting window for condData block

    def on_settingBtn_pressed(self):
        self.settingDialog.exec()


    # Confirm setting window

    def on_settingDialog_accepted(self):
        self.settingDialog.hide()


    # Cancel setting window

    def on_settingDialog_rejected(self):
        self.settingDialog.hide()


        



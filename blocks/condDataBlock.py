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
        self.le = QtWidgets.QLineEdit(self.settingDialog)
        self.settingLayout.addWidget(self.le)


    ####################
    #      Slots
    ####################

    # Popup setting window for condData block

    def on_settingBtn_pressed(self):
        
        self.__leStr = self.le.text()
        self.settingDialog.exec()


    # Confirm setting window

    def on_settingDialog_accepted(self):
        pass


    # Cancel setting window

    def on_settingDialog_rejected(self):
        # Reset to old values
        self.le.setText(self.__leStr)
        


        



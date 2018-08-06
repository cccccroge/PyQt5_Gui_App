from PyQt5 import QtWidgets

class properties(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        vboxLayout = QtWidgets.QVBoxLayout()
        self.setLayout(vboxLayout)

        # Head
        headWidget = QtWidgets.QWidget()
        p1 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p1.setVerticalStretch(2)
        headWidget.setSizePolicy(p1)
        
        gridLayout = QtWidgets.QGridLayout()
        comboBox = QtWidgets.QComboBox()
        #labelImage = QtWidgets.QLabel()
        labelText2 = QtWidgets.QLabel()
        labelText = QtWidgets.QLabel()

        # List
        listWidget = QtWidgets.QWidget()
        p2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p2.setVerticalStretch(12)
        listWidget.setSizePolicy(p2)
        l2 = QtWidgets.QLabel(listWidget)
        l2.setText("2")

        # Button
        connectButton = QtWidgets.QPushButton()
        connectButton.setText(self.tr("建立聯結\n(+2項目)"))
        p3 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        p3.setVerticalStretch(2)
        connectButton.setSizePolicy(p3)


        vboxLayout.addWidget(headWidget)
        vboxLayout.addWidget(listWidget)
        vboxLayout.addWidget(connectButton)


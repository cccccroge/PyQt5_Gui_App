from PyQt5 import QtWidgets, QtCore, QtGui

class list(QtWidgets.QListWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.parent.list = self
        self.itemPressed.connect(self.on_itemPressed)


    # Show cols for provided file

    def showFile(self, filename):
        names = self.parent.colNamesSet[filename]

        self.clear()
        for n in names:
            item = QtWidgets.QListWidgetItem()
            item.setText(n)
            self.addItem(item)


    # Show cols that contains provided text

    def showSearch(self, searchText):
        # Make all item invisible
        for i in range(self.count()):
            self.item(i).setHidden(True)

        # Show the matches
        items = self.findItems(searchText, QtCore.Qt.MatchContains)
        for item in items:
            item.setHidden(False)



    ####################
    #      Slots
    ####################

    # Drag selected item to button for connection
    # Show result after D&D operation

    def on_itemPressed(self, item):
        # Parse info to (file + sheet + col) name
        colName = item.text()

        keyName = self.parent.comboBox.currentText()
        fileName = ""
        sheetName = ""

        index = keyName.find(" ： ")
        if index == -1:
            fileName = keyName
        else:
            fileName = keyName[0:index]
            sheetName = keyName[index+3:]

        # Create drag object and execute
        drag = QtGui.QDrag()
        data = QtCore.QMimeData()
        data.setText(fileName + "," + sheetName + "," + keyName)
        drag.setMimeData(data)

        ret = drag.exec(QtCore.Qt.LinkAction)

            
        
            
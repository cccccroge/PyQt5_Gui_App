import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import pickle

import properties
import field
import targetValBlock
from globalUsed import msgDuration

class central(QtWidgets.QTabWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # Store mainWindow to use in slots
        self.mainWindow = parent

        # Set tabWidget properties
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabCloseRequested.connect(self.on_tabCloseRequested)
        parent.setCentralWidget(self)

        # ITRI: we need easier interface (loaded default)
        parent.easyWidget = QtWidgets.QWidget()

        self.gridLayout = QtWidgets.QGridLayout()
        parent.easyWidget.setLayout(self.gridLayout)

        # select part
        groupboxSelectFormat = QtWidgets.QGroupBox(self.tr("選擇輸出格式 (更改勾選後，再按一次生效)"))
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        sp.setVerticalStretch(5)
        groupboxSelectFormat.setSizePolicy(sp)
        groupboxSelectFormatLayout = QtWidgets.QHBoxLayout()
        groupboxSelectFormat.setLayout(groupboxSelectFormatLayout)

        btn_format1 = QtWidgets.QPushButton()
        btn_format1.pressed.connect(self.on_btn_format1_pressed)
        btn_format1.setText(self.tr("附件二"))
        btn_format2 = QtWidgets.QPushButton()
        btn_format2.pressed.connect(self.on_btn_format2_pressed)
        btn_format2.setText(self.tr("專利清查"))
        btn_format2_2 = QtWidgets.QPushButton()
        btn_format2_2.pressed.connect(self.on_btn_format2_2_pressed)
        btn_format2_2.setText(self.tr("授權資料"))
        btn_format3 = QtWidgets.QPushButton()
        btn_format3.pressed.connect(self.on_btn_format3_pressed)
        btn_format3.setText(self.tr("專利清單"))
        btn_format4 = QtWidgets.QPushButton()
        btn_format4.pressed.connect(self.on_btn_format4_pressed)
        btn_format4.setText(self.tr("計價格式"))
        btn_format5 = QtWidgets.QPushButton()
        btn_format5.pressed.connect(self.on_btn_format5_pressed)
        btn_format5.setText(self.tr("計價表格"))

        sp2 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        sp2.setVerticalStretch(2)
        btn_format1.setSizePolicy(sp2)
        btn_format2.setSizePolicy(sp2)
        btn_format2_2.setSizePolicy(sp2)
        btn_format3.setSizePolicy(sp2)
        btn_format4.setSizePolicy(sp2)
        btn_format5.setSizePolicy(sp2)

        bigFont = QtGui.QFont()
        bigFont.setPointSize(18)
        bigFont.setBold(True)
        btn_format1.setFont(bigFont)
        btn_format2.setFont(bigFont)
        btn_format2_2.setFont(bigFont)
        btn_format3.setFont(bigFont)
        btn_format4.setFont(bigFont)
        btn_format5.setFont(bigFont)

        groupboxSelectFormatLayout.addWidget(btn_format1, QtCore.Qt.AlignCenter)
        groupboxSelectFormatLayout.addWidget(btn_format2, QtCore.Qt.AlignCenter)
        groupboxSelectFormatLayout.addWidget(btn_format2_2, QtCore.Qt.AlignCenter)
        groupboxSelectFormatLayout.addWidget(btn_format3, QtCore.Qt.AlignCenter)
        groupboxSelectFormatLayout.addWidget(btn_format4, QtCore.Qt.AlignCenter)
        groupboxSelectFormatLayout.addWidget(btn_format5, QtCore.Qt.AlignCenter)
        self.gridLayout.addWidget(groupboxSelectFormat, 0, 0)

        # target vals part
        groupboxTargetVals = QtWidgets.QGroupBox(self.tr("填入目標值"))
        sp3 = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred
                                   , QtWidgets.QSizePolicy.Preferred)
        sp3.setVerticalStretch(15)
        groupboxTargetVals.setSizePolicy(sp3)
        groupboxTargetValsLayout = QtWidgets.QVBoxLayout()
        groupboxTargetVals.setLayout(groupboxTargetValsLayout)

        self.checkbox_p40_patentno = QtWidgets.QCheckBox()
        self.checkbox_p40_patentno.setText(self.tr("件編號"))
        self.checkbox_p40_patentno.setChecked(True)
        self.checkbox_p40_patentno.stateChanged.connect(self.on_checkbox_p40_patentno_stateChanged)
        self.checkbox_p40_applypntno = QtWidgets.QCheckBox()
        self.checkbox_p40_applypntno.setText(self.tr("申請案號"))
        self.checkbox_p40_applypntno.stateChanged.connect(self.on_checkbox_p40_applypntno_stateChanged)
        self.targetValsEdit = QtWidgets.QTextEdit()
        okToChangeValsBtn = QtWidgets.QPushButton()
        okToChangeValsBtn.setFixedSize(100, 50)
        okToChangeValsBtn.setText(self.tr("確認"))
        okToChangeValsBtn.pressed.connect(self.on_okToChangeValsBtn_pressed)
        outputBtn = QtWidgets.QPushButton()
        outputBtn.setFixedSize(100, 50)
        outputBtn.setText(self.tr("輸出"))
        outputBtn.pressed.connect(self.on_outputBtn_pressed)
        groupboxTargetValsLayout.addWidget(self.checkbox_p40_patentno, QtCore.Qt.AlignCenter)
        groupboxTargetValsLayout.addWidget(self.checkbox_p40_applypntno, QtCore.Qt.AlignCenter)
        groupboxTargetValsLayout.addWidget(self.targetValsEdit, QtCore.Qt.AlignCenter)
        groupboxTargetValsLayout.addWidget(okToChangeValsBtn)
        groupboxTargetValsLayout.addWidget(outputBtn)
        self.gridLayout.addWidget(groupboxTargetVals, 1, 0)

        self.addTab(parent.easyWidget, self.tr("簡易介面"))

        # Main work space 
        parent.mainWidget = QtWidgets.QSplitter()   # make field of mainWindow to access mainWidget in other places
        
        propertiesWidget = properties.properties(parent)
        parent.mainWidget.addWidget(propertiesWidget)

        self.fieldWidget = field.field(parent)
        parent.mainWidget.addWidget(self.fieldWidget)

        parent.mainWidget.setSizes([320, 1600])
        self.addTab(parent.mainWidget, self.tr("樣板工作區"))

        
        # Test
        #w = QtWidgets.QWidget()
        #self.addTab(w, "2")



    ####################
    #      Slots
    ####################

    def on_tabCloseRequested(self, index):
        target = self.widget(index)

        # If is mainWidget/easyWidget, don't delete it, just hide
        if target == self.mainWindow.mainWidget or target == self.mainWindow.easyWidget:
            self.removeTab(index)
        else:
            target.deleteLater()
            self.removeTab(index)

    def on_checkbox_p40_patentno_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.checkbox_p40_applypntno.setChecked(False)

    def on_checkbox_p40_applypntno_stateChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.checkbox_p40_patentno.setChecked(False)
        
    def on_btn_format1_pressed(self):
        if self.checkbox_p40_patentno.checkState() == QtCore.Qt.Checked:
            path = ("./template/附件二樣板.ieb")
        else:
            path = ("./template/附件二樣板_使用申請案號.ieb")
        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.mainWindow.relatedGraph = graphTemplate
        self.mainWindow.buildBlocksUseData(blksDataTemplate)

        self.mainWindow.statusBar().showMessage("成功讀取樣板", msgDuration)

    def on_btn_format2_pressed(self):
        if self.checkbox_p40_patentno.checkState() == QtCore.Qt.Checked:
            path = ("./template/專利清查樣板.ieb")
        else:
            path = ("./template/專利清查樣板_使用申請案號.ieb")
        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.mainWindow.relatedGraph = graphTemplate
        self.mainWindow.buildBlocksUseData(blksDataTemplate)

        self.mainWindow.statusBar().showMessage("成功讀取樣板", msgDuration)

    def on_btn_format2_2_pressed(self):
        if self.checkbox_p40_patentno.checkState() == QtCore.Qt.Checked:
            path = ("./template/授權紀錄資料.ieb")
        else:
            path = ("./template/授權紀錄資料_使用申請案號.ieb")
        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.mainWindow.relatedGraph = graphTemplate
        self.mainWindow.buildBlocksUseData(blksDataTemplate)

        self.mainWindow.statusBar().showMessage("成功讀取樣板", msgDuration)

    def on_btn_format3_pressed(self):
        if self.checkbox_p40_patentno.checkState() == QtCore.Qt.Checked:
            path = ("./template/專利清單樣板.ieb")
        else:
            path = ("./template/專利清單樣板_使用申請案號.ieb")
        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.mainWindow.relatedGraph = graphTemplate
        self.mainWindow.buildBlocksUseData(blksDataTemplate)

        self.mainWindow.statusBar().showMessage("成功讀取樣板", msgDuration)

    def on_btn_format4_pressed(self):
        if self.checkbox_p40_patentno.checkState() == QtCore.Qt.Checked:
            path = ("./template/計畫格式樣板.ieb")
        else:
            path = ("./template/計畫格式樣板_使用申請案號.ieb")
        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.mainWindow.relatedGraph = graphTemplate
        self.mainWindow.buildBlocksUseData(blksDataTemplate)

        self.mainWindow.statusBar().showMessage("成功讀取樣板", msgDuration)

    def on_btn_format5_pressed(self):
        if self.checkbox_p40_patentno.checkState() == QtCore.Qt.Checked:
            path = ("./template/計價表格樣板.ieb")
        else:
            path = ("./template/計價表格樣板_使用申請案號.ieb")
        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.mainWindow.relatedGraph = graphTemplate
        self.mainWindow.buildBlocksUseData(blksDataTemplate)

        self.mainWindow.statusBar().showMessage("成功讀取樣板", msgDuration)

    def on_okToChangeValsBtn_pressed(self):
        plain = self.targetValsEdit.toPlainText()

        # Find template's TargetValueBlock
        TVB = None

        grid = self.fieldWidget.gridLayout
        for row in range(grid.rowCount() - 1):
            hboxLayout = grid.itemAtPosition(row, 0)
            for col in range(3, hboxLayout.count(), 2):  # start from 1st block and ignore dashes
                curBlk = hboxLayout.itemAt(col).widget()
                if type(curBlk) == targetValBlock.targetValBlock:
                    TVB = curBlk

        if TVB is None:
            self.mainWindow.statusBar().showMessage("無法套用，樣板中不存在目標值方塊", msgDuration)
            return

        # Change edit, and also settingData
        TVB.textEdit.setText(plain)

        TVB.settingData["targetVals"] = []
        vals = TVB.textEdit.toPlainText().split()
        for val in vals:
            TVB.settingData["targetVals"].append(val)

        print("settingData becomes: ")
        print(TVB.settingData)

    def on_outputBtn_pressed(self):
        # trigger menu's output action
        outputAction = self.mainWindow.actions["exportExcel"]
        outputAction.trigger()


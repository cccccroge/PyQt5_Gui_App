import sys
from PyQt5 import QtWidgets, QtCore
import pandas as pd
import numpy as np
import networkx as nx
import pickle
import datetime

import menu
import tool
import status
import central
from globalUsed import msgDuration, fieldRowHeight, make_red_font

import targetValBlock, dataBlock, multiDataBlock, condDataBlock
import dataFilterBlock, calculatorBlock, numberBlock, useAnotherBlock, defaultBlock
import styleBlock


class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.actions = {}
        self.colNamesSet = {}
        self.relatedGraph = nx.DiGraph()
        self.srcFiles = {}
        self.tempData = {}  # use to store intermediate data, providing user to drag to others

        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.init_ui()

        # connect workers' signal to mainWindow's slot
        self.importWorker = import_excel_thread(self)
        self.importWorker.progress.connect(self.update_progress)
        self.importWorker.message.connect(self.show_message)
        self.importWorker.hint.connect(self.show_hint)
        self.importWorker.addKey.connect(self.add_key)
        self.importWorker.openFile.connect(self.get_open_files)
        self.importWorker.progressBarRange.connect(self.set_progressBar_range)
        self.importWorker.progressBarVisible.connect(self.set_progressBar_visible)

        self.exportWorker = export_excel_thread(self)
        self.exportWorker.progress.connect(self.update_progress)
        self.exportWorker.progressBarRange.connect(self.set_progressBar_range)
        self.exportWorker.progressBarVisible.connect(self.set_progressBar_visible)
        self.exportWorker.message.connect(self.show_message)
        self.exportWorker.hint.connect(self.show_hint)


    def init_ui(self):
        # Sending mainWindow obj to initialize components
        # No need to store the objs because they're just init helper
        # Use parent-child relationship to access between classes
        self.menu = menu.menu(self)
        tool.tool(self)
        status.status(self)
        self.central = central.central(self)



    ####################
    # Action slots
    ####################

    def choose_work_dir(self):
        pass


    # Import selected excel, store columns info, excel path and file dataframes
    # After import, properties list should show sets of column name

    def import_excel_concurrent(self):
         # Get paths of selecting files
        filenamesList = [""]    # use another list to wrap the filenames, make it modifiable in another function
        self.get_open_files(filenamesList)
        filenames = filenamesList[0]

        # Start importing on another thread
        self.importWorker.setFilenames(filenames)
        self.importWorker.start()

    def export_excel_concurrent(self):
        # Select save file path
        fileName = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr("儲存檔案"), ""
            , "All Files (*);;Excel Files (*xlsx);;Excel 97-2003 Files(*xls)"
            , "Excel Files (*xlsx)")

        if fileName[0] == "":
            self.statusBar().showMessage("取消儲存檔案", msgDuration)
            return
        
        # Start exporting on another thread
        self.exportWorker.setFileName(fileName)
        self.exportWorker.start()


    def add_related_property(self):
        print("新增關聯項目")

    def load_template(self):
        # Select file to open
        fileNamesObj = QtWidgets.QFileDialog.getOpenFileNames(
            self, self.tr("讀取樣板"), "",
            self.tr("Excel In Blocks (*.ieb);;All Files (*)"),
            self.tr("Excel In Blocks (*.ieb)"))

        if len(fileNamesObj[0]) == 0:
            self.statusBar().showMessage("取消儲存或未命名檔案", msgDuration)
            return

        path = fileNamesObj[0][0]   # fileNamesObj[0] is list of paths
        if path.rfind(".ieb") == -1:
            path = path + ".ieb"

        loadFile = open(path, "rb")

        # Take out objs from .ieb
        objsList = pickle.load(loadFile)
        graphTemplate = objsList[0]
        blksDataTemplate = objsList[1]
        print("extract data:")
        print(blksDataTemplate)

        # Replace current setting
        self.relatedGraph = graphTemplate
        self.buildBlocksUseData(blksDataTemplate)

        self.statusBar().showMessage("成功讀取樣板", msgDuration)



    def save_template(self):
        # Save a file with extension '.ieb(Excel In Blocks)'
        saveFile = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr("儲存樣板"), "", 
            self.tr("Excel In Blocks (*.ieb);;All Files (*)"),
            self.tr("Excel In Blocks (*.ieb)"))

        if saveFile[0] =="":
            self.statusBar().showMessage(self.tr("取消儲存樣板"), msgDuration)
            return

        path = saveFile[0]
        if path.rfind(".ieb") == -1:
            path = path + ".ieb"
        openedFile = open(path, 'wb')

        # Write data to this file: current graph and gridLayout
        objsList = []
        objsList.append(self.relatedGraph)
        blocks = self.getBlocksRawData(self.central.fieldWidget.gridLayout)
        objsList.append(blocks)
        pickle.dump(objsList, openedFile)

        openedFile.close()
        self.statusBar().showMessage(self.tr("成功儲存樣板"), msgDuration)
            

    def view_excel(self):
        print("檢視excel...")

    def view_exported_excel(self):
        print("檢視輸出excel")

    def toggle_toolbar(self):
        if (self.toolBar.isVisible()):
            self.toolBar.setVisible(False)
            self.statusBar().showMessage("已關閉工具列", msgDuration)
        else:
            self.toolBar.setVisible(True)
            self.statusBar().showMessage("已開啟工作列", msgDuration)

    def toggle_main_panel(self):
        # Find main panel
        isClosed = True
        targetIndex = -1
        for i in range(self.centralWidget().count()):
            if (self.centralWidget().widget(i) == self.mainWidget):
                isClosed = False
                targetIndex = i

        # Close if found, otherwise add it again
        if not isClosed:
            self.centralWidget().removeTab(targetIndex)
        else:
            self.centralWidget().insertTab(0, self.mainWidget, self.tr("樣板工作區"))
            self.centralWidget().setCurrentWidget(self.mainWidget)



    ####################
    # Helper functions
    ####################

    def load_excel_and_return_columns(self, _fileObj, _fileName, _sheetname):
        print("reading sheet of the file from obj...")
        cols = None
        if _sheetname == 0:
            self.srcFiles[(_fileName, "")] = pd.read_excel(_fileObj, _sheetname)
            cols = self.srcFiles[(_fileName, "")].head(0)
        else:
            self.srcFiles[(_fileName, _sheetname)] = pd.read_excel(_fileObj, _sheetname)
            cols = self.srcFiles[(_fileName, _sheetname)].head(0)
        
        print("finish reading")

        return cols

    def getBlocksRawData(self, gridLayout):
        # Convert blocks data in gridLayout into packlible format
        data = {}
        for row in range(gridLayout.rowCount() - 1):
            hboxLayout = gridLayout.itemAtPosition(row, 0)
            col = 0
            while True:
                if col == 2:
                    col -= 1
                if hboxLayout.itemAt(col) is None:
                    break

                data[(row, col)] = {}   # 'position' map to 'data dict'
                curBlk = hboxLayout.itemAt(col).widget()

                # fill data dict depends on its type
                dict = data[(row, col)]
                print("converting blk to raw data: ({0}, {1})".format(row, col))
                if type(curBlk) == targetValBlock.targetValBlock:
                    print("type: targetValBlock")
                    dict["blkType"] = "targetValBlock"
                    dict["colSource"] = curBlk.colSource
                    dict["settingData"] = curBlk.settingData
                    dict["text"] = curBlk.textEdit.toPlainText()
                elif type(curBlk) == dataBlock.dataBlock:
                    print("type: dataBlock")
                    dict["blkType"] = "dataBlock"
                    dict["colSource"] = curBlk.colSource
                elif type(curBlk) == multiDataBlock.multiDataBlock:
                    print("type: multiDataBlock")
                    dict["blkType"] = "multiDataBlock"
                    dict["colSource"] = curBlk.colSource
                elif type(curBlk) == condDataBlock.condDataBlock:
                    print("type: condDataBlock")
                    dict["blkType"] = "condDataBlock"
                    dict["settingData"] = curBlk.settingData
                    dict["existData"] = (curBlk.lineEditYes.text(),
                                            curBlk.lineEditNo.text())
                    dict["valData"] = []
                    grid = curBlk.groupBoxMaprulesLayout2
                    for mapRow in range(grid.rowCount()):
                        fromText = grid.itemAtPosition(mapRow, 0).widget().text()
                        toText = grid.itemAtPosition(mapRow, 2).widget().text()
                        dict["valData"].append((fromText, toText))

                    dict["formData"] = (curBlk.limitEdit.colSource, 
                                        curBlk.limitEdit.text(),
                                        curBlk.fromEdit.colSource,
                                        curBlk.toEdit.colSource)
                elif type(curBlk) == dataFilterBlock.dataFilterBlock:
                    print("type: dataFilterBlock")
                    dict["blkType"] = "dataFilterBlock"
                    dict["colSource"] = curBlk.colSource
                    dict["settingData"] = curBlk.settingData
                elif type(curBlk) == numberBlock.numberBlock:
                    print("type: numberBlock")
                    dict["blkType"] = "numberBlock"
                elif type(curBlk) == calculatorBlock.calculatorBlock:
                    print("type: calculatorBlock")
                    dict["blkType"] = "calculatorBlock"
                    dict["settingData"] = curBlk.settingData
                elif type(curBlk) == useAnotherBlock.useAnotherBlock:
                    print("type: useAnotherBlock")
                    dict["blkType"] = "useAnotherBlock"
                elif type(curBlk) == defaultBlock.defaultBlock:
                    print("type: defaultBlock")
                    dict["blkType"] = "defaultBlock"
                    dict["settingData"] = curBlk.settingData
                elif type(curBlk) == styleBlock.styleBlock:
                    print("type: styleBlock")
                    dict["blkType"] = "styleBlock"
                elif type(curBlk) == QtWidgets.QLineEdit:
                    print("type: lineEdit")
                    dict["editText"] = curBlk.text()

                col += 2

        return data
        
        

    def buildBlocksUseData(self, data):
        # Clear current gridLayout
        self.clearItemsInGrid(self.central.fieldWidget.gridLayout)
        self.central.fieldWidget.vboxLayout2.removeItem(
            self.central.fieldWidget.gridLayout)
        self.central.fieldWidget.gridLayout.deleteLater()
       
        addColBtn = QtWidgets.QPushButton()
        addColBtn.setText("+")
        addColBtn.setFixedSize(25, 25)
        addColBtn.pressed.connect(self.central.fieldWidget.on_addColBtn_pressed)
        
        grid = QtWidgets.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)
        grid.setContentsMargins(25, 25, 25, 25)
        grid.setVerticalSpacing(25)
        grid.setHorizontalSpacing(0)
        grid.addWidget(addColBtn, 0, 0, QtCore.Qt.AlignLeft)

        self.central.fieldWidget.gridLayout = grid
        self.central.fieldWidget.vboxLayout2.insertLayout(0, grid)

        # Rebuild blocks using data
        for key, val in data.items():
            print("key is {0}".format(key))
            print("val is {0}".format(val))

            row = key[0]
            col = key[1]
            dataDict = val

            # not block, is lineEdit
            if "blkType" not in dataDict and col != 0:
                idEdit = QtWidgets.QLineEdit()
                idEdit.setText(str(row + 1))
                idEdit.setAlignment(QtCore.Qt.AlignCenter)
                idEdit.setFixedSize(25, fieldRowHeight)
                idEdit.setReadOnly(True)

                le = QtWidgets.QLineEdit()
                le.setPlaceholderText(self.tr("欄位名稱"))
                le.setText(dataDict["editText"])
                le.setFixedSize(QtCore.QSize(125, fieldRowHeight))

                hboxLayout = None
                if type(grid.itemAtPosition(row, 0)) == \
                    QtWidgets.QHBoxLayout:
                    hboxLayout = grid.itemAtPosition(row, 0)
                    hboxLayout.addWidget(idEdit, 0, QtCore.Qt.AlignLeft)
                    hboxLayout.addWidget(le, 0, QtCore.Qt.AlignLeft)
                else:   # this row is addColBtn, extend row
                    hboxLayout = QtWidgets.QHBoxLayout()
                    hboxLayout.setContentsMargins(0, 0, 0, 0)
                    hboxLayout.setSpacing(0)
                    addColBtn = grid.itemAtPosition(row, 0).widget()
                    grid.addLayout(hboxLayout, row, 0, QtCore.Qt.AlignLeft)
                    grid.addWidget(addColBtn, row + 1, 0, QtCore.Qt.AlignLeft)
                    hboxLayout.addWidget(idEdit, 0, QtCore.Qt.AlignLeft)
                    hboxLayout.addWidget(le, 0, QtCore.Qt.AlignLeft)

                continue

            # is block, create corresponding block
            blk = self.buildBlock(dataDict, row)
            if blk is None:
                continue
            
            if type(grid.itemAtPosition(row, 0)) == \
                    QtWidgets.QHBoxLayout:
                hboxLayout = grid.itemAtPosition(row, 0)
                hboxLayout.insertWidget(col, blk, 0, QtCore.Qt.AlignLeft)
            else:
                hboxLayout = QtWidgets.QHBoxLayout()
                hboxLayout.setContentsMargins(0, 0, 0, 0)
                hboxLayout.setSpacing(0)
                addColBtn = grid.itemAtPosition(row, 0).widget()
                grid.addLayout(hboxLayout, row, 0, QtCore.Qt.AlignLeft)
                grid.addWidget(addColBtn, row + 1, QtCore.Qt.AlignLeft)

                hboxLayout.insertWidget(col, blk, 0, QtCore.Qt.AlignLeft)
        
        # Add back dashes
        for row in range(grid.rowCount() - 1): # should be rowCount, but rowCount doesn't update after deleting some rows
                hboxLayout = grid.itemAtPosition(row, 0)

                # don't need dash if no trailing blks
                if hboxLayout.count() == 1:
                    continue

                col = 2
                while col != hboxLayout.count(): 
                    lineLabel = QtWidgets.QLabel()
                    lineLabel.setText("──")
                    lineLabel.setFixedHeight(fieldRowHeight)
                    hboxLayout.insertWidget(col, lineLabel, 0, QtCore.Qt.AlignLeft)
                    col += 2


    def buildBlock(self, dataDict, hboxRow):
        if "blkType" not in dataDict:
            return

        blk = None
        type = dataDict["blkType"]

        if type == "targetValBlock":
            blk = targetValBlock.targetValBlock(self, self.central.fieldWidget)
            blk.colSource = dataDict["colSource"]
            blk.settingData = dataDict["settingData"]
            blk.textEdit.setText(dataDict["text"])

        elif type == "dataBlock":
            blk = dataBlock.dataBlock(self, self.central.fieldWidget)
            blk.colSource = dataDict["colSource"]
        elif type == "multiDataBlock":
            blk = multiDataBlock.multiDataBlock(self, self.central.fieldWidget)
            blk.colSource = dataDict["colSource"]
            for e in blk.colSource:
                item = QtWidgets.QListWidgetItem()
                item.setText(e)
                blk.showColList.addItem(item)
        elif type == "condDataBlock":
            blk = condDataBlock.condDataBlock(self, self.central.fieldWidget)
            blk.settingData = dataDict["settingData"]
            dataType = dataDict["settingData"]["dataType"]
            if dataType != "":
                id = 0 if dataType == "existence" else (1 if dataType == "value" else 2)
                radioBtn = blk.radioBtnGroup.button(id)
                radioBtn.setChecked(True)
                # remember enable the groupBox
                if id == 0:     
                    blk.groupBoxMaprules2.hide()
                    blk.groupBoxMapUseform.hide()
                    blk.groupBoxMaprules.show()
                elif id == 1:
                    blk.groupBoxMaprules.hide()
                    blk.groupBoxMapUseform.hide()
                    blk.groupBoxMaprules2.show()
                elif id == 2:
                    blk.groupBoxMaprules.hide()
                    blk.groupBoxMaprules2.hide()
                    blk.groupBoxMapUseform.show()

            blk.lineEditYes.setText(dataDict["existData"][0])
            blk.lineEditNo.setText(dataDict["existData"][1])

            layoutOfVals = blk.groupBoxMaprulesLayout2
            for row in range(len(dataDict["valData"])):
                text1 = dataDict["valData"][row][0]
                text2 = dataDict["valData"][row][1]
                layoutOfVals.itemAtPosition(row, 0).widget().setText(text1)
                layoutOfVals.itemAtPosition(row, 2).widget().setText(text2)
            
            blk.limitEdit.colSource = dataDict["formData"][0]
            blk.limitEdit.setText(dataDict["formData"][1])
            blk.fromEdit.colSource = dataDict["formData"][2]
            if dataDict["formData"][2] is not None:
                blk.fromEdit.setText(dataDict["formData"][2][2])
            blk.toEdit.colSource = dataDict["formData"][3]
            if dataDict["formData"][3] is not None:
                blk.toEdit.setText(dataDict["formData"][3][2])

        elif type == "dataFilterBlock":
            blk = dataFilterBlock.dataFilterBlock(self, self.central.fieldWidget)
            blk.colSource = dataDict["colSource"]
            blk.settingData = dataDict["settingData"]

            blk.lineEditSatisfy.colSource = dataDict["settingData"]["satisfyCol"]
            blk.lineEditSatisfy.setText(dataDict["settingData"]["satisfyCond"])
            dataType = dataDict["settingData"]["dataType"]
            blk.origCheckbox.setChecked(dataDict["settingData"]["origChecked"])
            if dataType != "":
                id = 0 if dataType == "str" else (1 if dataType == "num" else 2)
                radioBtn = blk.radioBtnGroup.button(id)
                radioBtn.setChecked(True)
            blk.lineEditCond.setText(dataDict["settingData"]["filterCond"])

        elif type == "numberBlock":
            blk = numberBlock.numberBlock(self, self.central.fieldWidget)
        elif type == "calculatorBlock":
            blk = calculatorBlock.calculatorBlock(self, self.central.fieldWidget)
            blk.settingData = dataDict["settingData"]
            blk.useExcelCheckbox.setChecked(dataDict["settingData"]["useExcelFormula"])
            blk.formulaEdit.setText(dataDict["settingData"]["formula"])

            method = dataDict["settingData"]["approxMethod"]
            if method == "round":
                blk.approxMethodCombo.setCurrentIndex(0)
            elif method == "ceil":
                blk.approxMethodCombo.setCurrentIndex(1)
            elif method == "floor":
                blk.approxMethodCombo.setCurrentIndex(2)

            blk.approxDigitSpin.setValue(dataDict["settingData"]["approxDigit"])

        elif type == "useAnotherBlock":
            blk = useAnotherBlock.useAnotherBlock(self, self.central.fieldWidget)
        elif type == "defaultBlock":
            blk = defaultBlock.defaultBlock(self, self.central.fieldWidget)
            blk.settingData = dataDict["settingData"]
            blk.useNumber.setChecked(dataDict["settingData"]["useNum"])
            blk.valEdit.setText(dataDict["settingData"]["val"])
        elif type == "styleBlock":
            blk = styleBlock.styleBlock(self, self.central.fieldWidget)
        else:
            return

        blk.setMouseTracking(True)
        blk.created = True
        blk.putRow = hboxRow
        blk.nameEdit.setDisabled(True)
        blk.nameEdit.setReadOnly(True)

        return blk


    def clearItemsInGrid(self, grid):
        for row in range(grid.rowCount()):
            for col in range(grid.columnCount()):
                item = grid.itemAtPosition(row, col)
                # delete all element in hboxLayout & layout itself
                if type(item) == QtWidgets.QHBoxLayout:
                    for i in range(item.count()):
                        widget = item.itemAt(i).widget() # must be all wigets
                        widget.deleteLater()
                    grid.removeItem(item)
                    item.deleteLater()
                # delete addBtn
                else:
                    item.widget().deleteLater()



    ####################
    # Slots
    ####################

    def update_progress(self, float):
        self.progressBar.setValue(float)

    def show_message(self, str):
        self.statusBar().showMessage(str, msgDuration)

    def show_hint(self, str):
        self.hintLabel.setText(str)

    def add_key(self, str):
        self.comboBox.addItem(str)

    def get_open_files(self, filenamesList):
        filenamesList[0] = QtWidgets.QFileDialog.getOpenFileNames(
            self, self.tr("選取檔案"), ""
            , "All Files (*);;Excel Files (*xlsx);;Excel 97-2003 Files(*xls)"
            , "All Files (*)")

    def set_progressBar_range(self, f1, f2):
        self.progressBar.setRange(f1, f2)

    def set_progressBar_visible(self, boolean):
        self.progressBar.setVisible(boolean)


class import_excel_thread(QtCore.QThread):
    progress = QtCore.pyqtSignal(float)
    message = QtCore.pyqtSignal(str)
    hint = QtCore.pyqtSignal(str)
    addKey = QtCore.pyqtSignal(str)
    openFile = QtCore.pyqtSignal(list)
    progressBarRange = QtCore.pyqtSignal(float, float)
    progressBarVisible = QtCore.pyqtSignal(bool)
    
    def __init__(self, caller, parent=None):
        super(import_excel_thread, self).__init__(parent)
        self.obj = caller
        self.filenames = None

    def setFilenames(self, filenames):
        self.filenames = filenames

    def run(self):
        # filenames is the list get from 'getOpenFileNames'
        filenames = self.filenames

        if len(filenames) == 0:
            self.message.emit("取消讀取或未選取檔案")
            print("yoyo")
            return

        excelPaths = []
        for n in filenames[0]:
            excelPaths.append(n)

        # Covert each sheet of files to set of column names
        self.message.emit("已選擇 " + str(len(excelPaths)) + " 個檔案")
        self.hint.emit("正在讀取檔案...")
        self.progressBarRange.emit(0, len(excelPaths))
        self.progress.emit(0)
        self.progressBarVisible.emit(True)

        newKeys = []
        isDuplicated = False

        for i in range(len(excelPaths)):
            print("reading a file to obj...")
            fileObj = pd.ExcelFile(excelPaths[i])
            sheetNames = fileObj.sheet_names
            print("finish reading")
            if (len(sheetNames) == 1):
                # No sheet name provided, use file name as key
                path = excelPaths[i]
                pos1 = path.rfind("/")
                pos2 = path.rfind(".xls")
                fileName = path[pos1 + 1 : pos2]
                fileName = self.convertSpecialNameToFitTemplate(fileName)
                if fileName in self.obj.colNamesSet.keys():
                    isDuplicated = True
                else:
                    newKeys.append(fileName)
                    self.obj.colNamesSet[fileName] = \
                        self.obj.load_excel_and_return_columns(fileObj, fileName, 0)
            else:
                # Multiple sheets, use (file ： sheet) name as key
                for sheetName in sheetNames:
                    path = excelPaths[i]
                    pos1 = path.rfind("/")
                    pos2 = path.rfind(".xls")
                    fileName = path[pos1 + 1 : pos2]
                    fileName = self.convertSpecialNameToFitTemplate(fileName)
                    keyName = fileName + " ： " + sheetName

                    if keyName in self.obj.colNamesSet.keys():
                        isDuplicated = True
                    else:
                        newKeys.append(keyName)
                        self.obj.colNamesSet[keyName] = \
                            self.obj.load_excel_and_return_columns(fileObj, fileName, sheetName)

            self.progress.emit(i + 1)

        # Add new file names to combobox
        for key in newKeys:
            self.addKey.emit(key)

        self.hint.emit("就緒")
        self.progressBarVisible.emit(False)

        if isDuplicated:
            self.message.emit("檔案讀取時發現重複的檔案或表單名稱，該部分已自動忽略")
        else:
            self.message.emit("檔案讀取成功")

    def convertSpecialNameToFitTemplate(self, fileName):
        if fileName.find("科專成果盤點") != -1:
            fileName = "FY90-107科專成果盤點 (武昌)FY107僅列科專計畫編號 1070918"
        elif fileName.find("專利暨可移轉技術資料") != -1:
            fileName =  "專利暨可移轉技術資料對照表-v.20180508(欣唐)"
        elif fileName.find("科專計畫編號對應ITRI計畫代號") != -1:
            fileName = "彙總 90-107 科專計畫編號對應ITRI計畫代號(1070908)"
        elif fileName.find("加值歷史紀錄") != -1:
            fileName = "過去加值歷史紀錄"

        return fileName



class export_excel_thread(QtCore.QThread):
    progress = QtCore.pyqtSignal(float)
    progressBarRange = QtCore.pyqtSignal(float, float)
    progressBarVisible = QtCore.pyqtSignal(bool)
    message = QtCore.pyqtSignal(str)
    hint = QtCore.pyqtSignal(str)

    def __init__(self, caller, **kwargs):
        super(export_excel_thread, self).__init__(**kwargs)
        self.obj = caller
        self.fileName = None

    def setFileName(self, filename):
        self.fileName = filename

    def run(self):
        # 1.Empty two-dimen list
        outputForm = [] # will append lists into it
        outputDf = None # use outputForm as input, will eventually convert to excel

        # 2.Fill all output column names
        grid = self.obj.central.fieldWidget.gridLayout

        colNamesList = []
        for row in range(grid.rowCount() - 1):
            hboxLayout = grid.itemAtPosition(row, 0)
            colName = hboxLayout.itemAt(1).widget().text()
            colNamesList.append(colName)
        outputForm.append(colNamesList)  

        # 3.Fill data by parsing field blocks & relation graph info
        # 3-1.find the tagetValBlock's info
        valColSrc = None
        valsList = None

        num_target = 0
        num_total = 0
        for row in range(grid.rowCount() - 1):
            hboxLayout = grid.itemAtPosition(row, 0)
            if hboxLayout.count() >= 3:
                num_total += 1

            for col in range(3, hboxLayout.count(), 2):  # start from 1st block and ignore dashes
                curBlk = hboxLayout.itemAt(col).widget()
                if type(curBlk) == targetValBlock.targetValBlock:
                    num_target += 1
                    valColSrc = curBlk.colSource
                    valsList = curBlk.settingData["targetVals"]

        # Consider invalid targetValBlk
        if num_target == 0:
            self.message.emit("輸出錯誤：不存在目標值方塊")
            return
        elif num_target > 1:
            self.message.emit("輸出錯誤：目標值方塊不唯一")
            return
        else:
            if valColSrc is None:
                self.message.emit("輸出錯誤：沒有指定目標值欄位")
                return
            if (valsList is None) or len(valsList) == 0:
                self.message.emit("輸出錯誤：沒有指定目標值")
                return

        # Consider only two rows(special form for single target val)
        twoRowCase = False
        if num_total == 2:
            twoRowCase = True

        # Force changing valsList if valColSrc is special case (not p40_patentno)
        # 申請案號：first find p40_applypntno contains, 
        #          use that row's p40_oripntno to gen p40_patentno

        # fix: find all p40_patentno in those rows of according p40_applypntno
        if valColSrc[2] == "p40_applypntno":
            valColSrc = "dbo_pat040", "dbo_pat0401", "p40_patentno"

            valsList_new = []
            for val in valsList:
                DFB_contains = dataFilterBlock.dataFilterBlock(self.obj, self.obj.central.fieldWidget)
                DFB_contains.colSource = "dbo_pat040", "dbo_pat0401", "p40_applypntno"
                DFB_contains.settingData["dataType"] = "str"
                DFB_contains.settingData["filterCond"] = "contains " + val
                print("now settingDatap['filterCond'] is: {0}".format(DFB_contains.settingData["filterCond"]))
                DFB_contains.settingData["origChecked"] = True
                out, outColSrc, msg = DFB_contains.generateOut(
                    None, DFB_contains.colSource, self.obj.relatedGraph)
                print("Atfer DFB_contains, out is:")
                print(out)

                #DB_getOri = dataBlock.dataBlock(self.obj, self.obj.central.fieldWidget)
                #DB_getOri.colSource = "dbo_pat040", "dbo_pat0401", "p40_oripntno"
                #out, outColSrc, msg = DB_getOri.generateOut(out, outColSrc, self.obj.relatedGraph)
                #print("Atfer DB_getOri, out is:")
                #print(out)

                #DFB_getPat = dataFilterBlock.dataFilterBlock(self.obj, self.obj.central.fieldWidget)
                #DFB_getPat.colSource = "dbo_pat040", "dbo_pat0401", "p40_patentno"
                #DFB_getPat.settingData["dataType"] = "str"
                #if out is None:
                #    out = ""
                #DFB_getPat.settingData["filterCond"] = "contains " + out
                #DFB_getPat.settingData["origChecked"] = True
                #out, outColSrc, msg = DFB_getPat.generateOut(
                #    None, DFB_getPat.colSource, self.obj.relatedGraph)
                #print("Atfer DFB_getPat, out is:")
                #print(out)

                MDB_purePat = multiDataBlock.multiDataBlock(self.obj, self.obj.central.fieldWidget)
                MDB_purePat.colSource = "p40_patentno"
                out, outColSrc, msg = MDB_purePat.generateOut(
                    out, MDB_purePat.colSource, self.obj.relatedGraph)
                print("Atfer MDB_purePat, out is:")
                print(out)

                #out = out.iloc[:,0]
                if out is not None:
                    out = out.tolist()
                    valsList_new.extend(out)

            valsList = valsList_new


        # 3-2.init progressBar range
        self.hint.emit("正在輸出檔案...")
        if twoRowCase:
            self.progressBarRange.emit(0, 1)
        else:
            self.progressBarRange.emit(0, len(valsList) * (grid.rowCount() - 1))
        self.progress.emit(0)
        self.progressBarVisible.emit(True)
        finishNum = 0

        # 3-3.start parsing
        valRow = 0   # used in calculatorBlk
        changeStyleCells = []   # change style on these element at final stage
        for idx, val in enumerate(valsList):
            valRow += 1
            # find start rows as beginning point
            fileDf = self.obj.srcFiles[(valColSrc[0], valColSrc[1])]
            colName = valColSrc[2]
            startRows = fileDf.loc[fileDf[colName] == val]

            # parse single row
            rowDataList = []
            for row in range(grid.rowCount() - 1):
                hboxLayout = grid.itemAtPosition(row, 0)

                print("\n row = {0}".format(row))
                # start parsing...
                out = startRows
                style = "default"
                outColSrc = valColSrc
                errorMsg = ""
                errorPos = ()

                for col in range(3, hboxLayout.count(), 2):
                    curBlk = hboxLayout.itemAt(col).widget()

                    # change out data
                    if type(curBlk) == useAnotherBlock.useAnotherBlock:
                        out, outColSrc, newMsg = curBlk.generateOut(out, startRows, valColSrc)
                        if outColSrc is None:   # has value, use this val
                            errorMsg = newMsg
                            break
                        else:
                            errorMsg += ("\n" + newMsg)
                            errorPos = (row, col)
                            continue    # no value, consider next
                    elif type(curBlk) == condDataBlock.condDataBlock:
                        out, errorMsg = curBlk.generateOut(out)
                        if out is None:
                            errorPos = (row, col)

                    elif type(curBlk) == numberBlock.numberBlock:
                        out = curBlk.generateOut(out)
                    elif type(curBlk) == targetValBlock.targetValBlock: # should be alone
                        out = val
                        break
                    elif type(curBlk) == calculatorBlock.calculatorBlock: # assume alone
                        out, errorMsg = curBlk.generateOut(valRow)
                    elif type(curBlk) == dataBlock.dataBlock:
                        out, outColSrc, newMsg = \
                            curBlk.generateOut(out, outColSrc, self.obj.relatedGraph)
                        if out is None:
                            errorMsg += ("\n" + newMsg)
                            errorPos = (row, col)
                    elif type(curBlk) == multiDataBlock.multiDataBlock:
                        out, outColSrc, newMsg = \
                            curBlk.generateOut(out, outColSrc, self.obj.relatedGraph)
                        if out is None:
                            errorMsg += ("\n" + newMsg)
                            errorPos = (row, col)
                    elif type(curBlk) == dataFilterBlock.dataFilterBlock:
                        out, outColSrc, newMsg = \
                            curBlk.generateOut(out, outColSrc, self.obj.relatedGraph)
                        if out is None:
                            errorMsg += ("\n" + newMsg)
                            errorPos = (row, col)
                    elif type(curBlk) == defaultBlock.defaultBlock:
                        out, errorMsg = curBlk.generateOut()
                    elif type(curBlk) == styleBlock.styleBlock:
                        pass
                    else:
                        out = "you're not using any valid blocks, Bro"
                        break

                    # change style
                    if style != "red" and type(curBlk) == styleBlock.styleBlock:
                        style = "red"
                    elif style != "default" and type(curBlk) != styleBlock.styleBlock:
                        style = "default"

                # append final output val to get row list, and store to temp data dict
                data = None
                if hboxLayout.count() == 2: # no trailing blocks
                    data = ""
                    self.obj.tempData[str(row)] = data
                else:
                    if out is not None:
                        data = out
                        self.obj.tempData[str(row)] = data
                    else:
                        data = "N/A" + "\n最後錯誤發生在" \
                            + str(errorPos) + ":\n" + errorMsg  # leave N/A + reasons
                        self.obj.tempData[str(row)] = None

                    if type(data) == pd.core.frame.DataFrame \
                        or type(data) == pd.core.frame.Series:     
                        data = data.reset_index()
                        del data["index"]

                if twoRowCase and row == 1:   # means the only df
                    if outputDf is None:
                        outputDf = out
                    else:
                        outputDf = outputDf.append(out, ignore_index=True)
                    self.progress.emit(1)
                else:
                    rowDataList.append(data)
                    # finish one field row
                    finishNum += 1
                    self.progress.emit(finishNum)

                # record pos that need to change its style
                if style == "red":
                    pos = (idx + 1, row)    # first add one: consider cols header
                    changeStyleCells.append(pos)

                    print("pos '{0}' should be stylized.".format(pos))

            # append whole row list to get form matrix
            outputForm.append(rowDataList)
            

        # 4.Transfer to df for post edit: two-dimen list -> dataFrame
        if not twoRowCase:
            outputDf = pd.DataFrame(outputForm)

        # 5.Adjust the dataframe with specified output setting
        # 5-1 Change style for some cells
        if len(changeStyleCells) != 0:
            print("changing style...")
            try:
                outputDf = outputDf.style.apply(make_red_font, axis=None, target=changeStyleCells)
            except NotImplementedError:
                self.message.emit("無法將特殊算法欄位轉換為紅色")

        # 5-2 Sort df
        # TODO...

        ## 5-3 replace illegal character
        #outputDf = outputDf.applymap(lambda x: x.encode('unicode_escape').
        #         decode('utf-8') if isinstance(x, str) else x)

        # 6.Output to excel: dataFrame -> excel
        fileName = self.fileName

        lpos = fileName[1].rfind("(") + 2
        rpos = fileName[1].rfind(")")
        ext = "." + (fileName[1])[lpos:rpos]

        today = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        path = fileName[0]
        if path.find(ext) == -1:    # if user didn't type extension then add for them
            path = path  + "_" + today + ext
        else:   # has extension: insert date before .
            dot = path.rfind(".")
            path_1 = path[:dot]
            path_2 = path[dot:]
            path = path_1 + "_" + today + path_2

        writer = pd.ExcelWriter(path)

        if not twoRowCase:
            outputDf.to_excel(writer, self.obj.tr("工作表1"), header=False, index=False)
        else:
            if outputDf is None:
                outputDf = pd.DataFrame(columns=['N/A'])
            outputDf.to_excel(writer, self.obj.tr("工作表1"), header=True, index=False)

        writer.save()

        self.hint.emit("就緒")
        self.progressBarVisible.emit(False)

        self.message.emit("檔案儲存成功")
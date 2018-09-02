import sys
from PyQt5 import QtWidgets, QtCore
import pandas as pd
import numpy as np
import networkx as nx
import pickle

import menu
import tool
import status
import central
from glob import msgDuration, fieldRowHeight

import targetValBlock, dataBlock, condDataBlock
import dataFilterBlock, calculatorBlock, numberBlock, useAnotherBlock


class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.actions = {}
        self.colNamesSet = {}
        self.relatedGraph = nx.DiGraph()
        self.srcFiles = {}

        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.init_ui()


    def init_ui(self):
        # Sending mainWindow obj to initialize components
        # No need to store the objs because they're just init helper
        # Use parent-child relationship to access between classes
        menu.menu(self)
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

    def import_excel(self):
        # Get paths of selecting files
        filenames = QtWidgets.QFileDialog.getOpenFileNames(
            self, self.tr("選取檔案"), ""
            , "All Files (*);;Excel Files (*xlsx);;Excel 97-2003 Files(*xls)"
            , "All Files (*)")

        if len(filenames) == 0:
            self.statusBar().showMessage("取消讀取或未選取檔案", msgDuration)
            return

        excelPaths = []
        for n in filenames[0]:
            excelPaths.append(n)

        # Covert each sheet of files to set of column names
        self.statusBar().showMessage("已選擇 " + str(len(excelPaths)) + " 個檔案", msgDuration)
        self.hintLabel.setText("正在讀取檔案...")
        self.progressBar.setRange(0, len(excelPaths))
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)

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
                pos2 = excelPaths[i].rfind(".xls")
                fileName = path[pos1 + 1 : pos2]
                if fileName in self.colNamesSet.keys():
                    isDuplicated = True
                else:
                    newKeys.append(fileName)
                    self.colNamesSet[fileName] = \
                        self.load_excel_and_return_columns(fileObj, fileName, 0)
            else:
                # Multiple sheets, use (file ： sheet) name as key
                for sheetName in sheetNames:
                    path = excelPaths[i]
                    pos1 = path.rfind("/")
                    pos2 = excelPaths[i].rfind(".xls")
                    fileName = path[pos1 + 1 : pos2]
                    keyName = fileName + " ： " + sheetName

                    if keyName in self.colNamesSet.keys():
                        isDuplicated = True
                    else:
                        newKeys.append(keyName)
                        self.colNamesSet[keyName] = \
                            self.load_excel_and_return_columns(fileObj, fileName, sheetName)

            self.progressBar.setValue(i + 1)

        # Add new file names to combobox
        for key in newKeys:
            self.comboBox.addItem(key)

        self.hintLabel.setText("就緒")
        self.progressBar.setVisible(False)

        if isDuplicated:
            self.statusBar().showMessage("檔案讀取時發現重複的檔案或表單名稱，該部分已自動忽略"
                                         , msgDuration)
        else:
            self.statusBar().showMessage("檔案讀取成功", msgDuration)
        

    def export_excel(self):
        # Select save file path
        fileName = QtWidgets.QFileDialog.getSaveFileName(
            self, self.tr("儲存檔案"), ""
            , "All Files (*);;Excel Files (*xlsx);;Excel 97-2003 Files(*xls)"
            , "Excel Files (*xlsx)")

        if fileName[0] == "":
            self.statusBar().showMessage("取消儲存檔案", msgDuration)
            return


        # 1.Empty two-dimen list
        outputForm = [] # will append lists into it

        # 2.Fill all output column names
        grid = self.central.fieldWidget.gridLayout

        colNamesList = []
        for row in range(grid.rowCount() - 1):
            hboxLayout = grid.itemAtPosition(row, 0)
            colName = hboxLayout.itemAt(0).widget().text()
            colNamesList.append(colName)
        outputForm.append(colNamesList)  

        # 3.Fill data by parsing field blocks & relation graph info
        # 3-1.find the tagetValBlock's info
        valColSrc = None
        valsList = None

        num = 0
        for row in range(grid.rowCount() - 1):
            hboxLayout = grid.itemAtPosition(row, 0)
            for col in range(2, hboxLayout.count(), 2):  # start from 1st block and ignore dashes
                curBlk = hboxLayout.itemAt(col).widget()
                if type(curBlk) == targetValBlock.targetValBlock:
                    num += 1
                    valColSrc = curBlk.colSource
                    valsList = curBlk.settingData["targetVals"]

        if num == 0:
            self.statusBar().showMessage("輸出錯誤：不存在目標值方塊", msgDuration)
            return
        elif num > 1:
            self.statusBar().showMessage("輸出錯誤：目標值方塊不唯一", msgDuration)
            return
        else:
            if valColSrc is None:
                self.statusBar().showMessage("輸出錯誤：沒有指定目標值欄位", msgDuration)
                return

        # 3-2.init progressBar range
        self.hintLabel.setText("正在輸出檔案...")
        self.progressBar.setRange(0, len(valsList) * (grid.rowCount() - 1))
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        finishNum = 0

        # 3-3.start parsing
        for val in valsList:
            # find start rows as beginning point
            fileDf = self.srcFiles[(valColSrc[0], valColSrc[1])]
            colName = valColSrc[2]
            startRows = fileDf.loc[fileDf[colName] == val]

            # parse single row
            rowDataList = []
            for row in range(grid.rowCount() - 1):
                hboxLayout = grid.itemAtPosition(row, 0)

                # empty row: ignore it
                if hboxLayout.count() == 1:
                    continue

                print("\n row = {0}".format(row))
                # start parsing...
                out = startRows
                outColSrc = valColSrc
                for col in range(2, hboxLayout.count(), 2):
                    curBlk = hboxLayout.itemAt(col).widget()

                    # input is nothing: failed to gen valid out if no UAB/CDB trailed behind
                    if out is None:
                        if type(curBlk) == useAnotherBlock.useAnotherBlock:
                            out = startRows
                            outColSrc = valColSrc
                        elif type(curBlk) == condDataBlock.condDataBlock:   # should not be 3rd
                            out = curBlk.generateOut(out)
                        elif type(curBlk) == numberBlock.numberBlock:
                            out = curBlk.generateOut(out)
                        else:
                            continue
                    # input has valid values: generate output as next input
                    else:
                        if type(curBlk) == targetValBlock.targetValBlock: # should be alone
                            out = val
                            break
                        if type(curBlk) == calculatorBlock.calculatorBlock: # assume alone
                            out = curBlk.generateOut(hboxLayout, out, outColSrc, self.relatedGraph)
                            break
                        if type(curBlk) == useAnotherBlock.useAnotherBlock:
                            break

                        if type(curBlk) == dataBlock.dataBlock:
                            out, outColSrc = \
                                curBlk.generateOut(out, outColSrc, self.relatedGraph)
                        elif type(curBlk) == condDataBlock.condDataBlock:
                            out = curBlk.generateOut(out)
                        elif type(curBlk) == numberBlock.numberBlock:
                            out = curBlk.generateOut(out)
                        elif type(curBlk) == dataFilterBlock.dataFilterBlock:
                            out, outColSrc = \
                                curBlk.generateOut(out, outColSrc, self.relatedGraph)
                        else:
                            out = "哈"
                            break
                
                # append final output val to get row list
                data = out if (out is not None) else "N/A" # leave N/A as invalid val
                rowDataList.append(data)

            # append whole row list to get form matrix
            outputForm.append(rowDataList)

            # finish one row
            finishNum += 1
            self.progressBar.setValue(finishNum)

        # 4.Transfer to df for post edit: two-dimen list -> dataFrame
        outputDf = pd.DataFrame(outputForm)

        # 5.Adjust the dataframe with specified output setting

        # 6.Output to excel: dataFrame -> excel
        lpos = fileName[1].rfind("(") + 2
        rpos = fileName[1].rfind(")")
        ext = "." + (fileName[1])[lpos:rpos]
        path = fileName[0]
        if path.find(ext) == -1:    # if user didn't type extension then add for them
            path = path + ext
        writer = pd.ExcelWriter(path)

        outputDf.to_excel(writer, self.tr("工作表1"), header=False, index=False)
        writer.save()

        self.hintLabel.setText("就緒")
        self.progressBar.setVisible(False)

        self.statusBar().showMessage("檔案儲存成功", msgDuration)


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
            self.centralWidget().insertTab(0, self.mainWidget, self.tr("主要工作面板"))
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
                for col in range(0, hboxLayout.count(), 2):
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
                    elif type(curBlk) == condDataBlock.condDataBlock:
                        print("type: condDataBlock")
                        dict["blkType"] = "condDataBlock"
                        dict["settingData"] = curBlk.settingData
                        dict["existData"] = (curBlk.lineEditYes.text(),
                                             curBlk.lineEditNo.text())
                        dict["valData"] = []
                        grid = curBlk.groupBoxMaprulesLayout2
                        for row in range(grid.rowCount()):
                            fromText = grid.itemAtPosition(row, 0).widget().text()
                            toText = grid.itemAtPosition(row, 2).widget().text()
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
                    elif type(curBlk) == calculatorBlock.calculatorBlock:   # TODO
                        dict["blkType"] = "calculatorBlock"
                    elif type(curBlk) == useAnotherBlock.useAnotherBlock:
                        print("type: useAnotherBlock")
                        dict["blkType"] = "useAnotherBlock"
                    else:
                        print("type: lineEdit")
                        dict["colText"] = curBlk.text() # first col (lineEdit)

        return data
        
        

    def buildBlocksUseData(self, data):
        # Clear current gridLayout
        grid = self.central.fieldWidget.gridLayout

        for row in range(grid.rowCount() - 1):
                hboxLayout = grid.itemAtPosition(row, 0)
                if hboxLayout is None:
                    continue

                isWidget = False
                widget = None
                for col in range(0, hboxLayout.count()):
                    if not isWidget:
                        widget = hboxLayout.itemAt(0).widget()
                    else:
                        widget = hboxLayout.itemAt(0)

                    hboxLayout.removeWidget(widget)
                    widget.deleteLater()

        # Rebuild blocks using data
        lastRow = -1    # use later in removing trailing rows
        for key, val in data.items():
            print("key is {0}".format(key))
            print("val is {0}".format(val))

            row = key[0]
            lastRow = row
            col = key[1]
            dataDict = val

            # not block, is lineEdit
            if "blkType" not in dataDict:
                le = QtWidgets.QLineEdit()
                le.setPlaceholderText(self.tr("欄位名稱"))
                le.setText(dataDict["colText"])
                le.setFixedSize(QtCore.QSize(125, fieldRowHeight))

                hboxLayout = None
                if type(grid.itemAtPosition(row, 0)) == \
                    QtWidgets.QHBoxLayout:
                    hboxLayout = grid.itemAtPosition(row, 0)
                    hboxLayout.insertWidget(0, le, 0, QtCore.Qt.AlignLeft)
                else:   # this row is addColBtn
                    hboxLayout = QtWidgets.QHBoxLayout()
                    hboxLayout.setContentsMargins(0, 0, 0, 0)
                    hboxLayout.setSpacing(0)
                    addColBtn = grid.itemAtPosition(row, 0).widget()
                    grid.addLayout(hboxLayout, row, 0, QtCore.Qt.AlignLeft)
                    grid.addWidget(addColBtn, row + 1, 0, QtCore.Qt.AlignLeft)

                    hboxLayout.insertWidget(0, le, 0, QtCore.Qt.AlignLeft)

                continue

            # is block, create corresponding block
            blk = None
            if dataDict["blkType"] == "targetValBlock":
                blk = self.buildBlock(dataDict)
            elif dataDict["blkType"] == "dataBlock":
                blk = self.buildBlock(dataDict)
            elif dataDict["blkType"] == "condDataBlock":
                blk = self.buildBlock(dataDict)
            elif dataDict["blkType"] == "dataFilterBlock":
                blk = self.buildBlock(dataDict)
            elif dataDict["blkType"] == "numberBlock":
                blk = self.buildBlock(dataDict)
            elif dataDict["blkType"] == "calculatorBlock":
                blk = self.buildBlock(dataDict)
            elif dataDict["blkType"] == "useAnotherBlock":
                blk = self.buildBlock(dataDict)
            
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

        print("before removing rows: {0}".format(grid.rowCount()))
        print("before removing widgets: {0}".format(grid.count()))
        # Remove trailing rows
        hboxLayout = None
        if grid.rowCount() - 2 > lastRow:
            for row in range(lastRow + 1, grid.rowCount() - 1): # don't remove addBtn
                hboxLayout = grid.itemAtPosition(row, 0)

                isWidget = False
                widget = None
                for col in range(0, hboxLayout.count()):
                    if not isWidget:
                        widget = hboxLayout.itemAt(0).widget()
                    else:
                        widget = hboxLayout.itemAt(0)

                    hboxLayout.removeWidget(widget)
                    widget.deleteLater()
                grid.removeItem(hboxLayout)
                hboxLayout.deleteLater()
        print("before removing rows: {0}".format(grid.rowCount()))
        print("after removing widgets: {0}".format(grid.count()))

        ## Add back dashes
        for row in range(grid.count() - 1): # should be rowCount, but rowCount doesn't update after deleting some rows
                hboxLayout = grid.itemAtPosition(row, 0)

                # don't need dash if no trailing blks
                if hboxLayout.count() == 1:
                    continue

                col = 1
                while col != hboxLayout.count(): 
                    lineLabel = QtWidgets.QLabel()
                    lineLabel.setText("──")
                    lineLabel.setFixedHeight(fieldRowHeight)
                    hboxLayout.insertWidget(col, lineLabel, 0, QtCore.Qt.AlignLeft)
                    col += 2
                    print("whatup")


    def buildBlock(self, dataDict):
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
            dataType = dataDict["settingData"]["dataType"]
            if dataType != "":
                id = 0 if dataType == "str" else (1 if dataType == "num" else 2)
                radioBtn = blk.radioBtnGroup.button(id)
                radioBtn.setChecked(True)
            blk.lineEditCond.setText(dataDict["settingData"]["filterCond"])

        elif type == "numberBlock":
            blk = numberBlock.numberBlock(self, self.central.fieldWidget)
        elif type == "calculatorBlock":
            blk = calculatorBlock.calculatorBlock(self, self.central.fieldWidget)
        elif type == "useAnotherBlock":
            blk = useAnotherBlock.useAnotherBlock(self, self.central.fieldWidget)
        else:
            return

        blk.setMouseTracking(True)
        blk.nameEdit.setDisabled(False)

        return blk

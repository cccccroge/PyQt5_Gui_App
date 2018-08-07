import sys
from PyQt5 import QtWidgets
import pandas as pd

import menu
import tool
import status
import central
from glob import msgDuration


class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.actions = {}
        self.colNamesSet = {}

        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.init_ui()


    def init_ui(self):
        # Sending mainWindow obj to initialize components
        # No need to store the objs because they're just init helper
        # Use parent-child relationship to access between classes
        menu.menu(self)
        tool.tool(self)
        status.status(self)
        central.central(self)



    ####################
    # Action slots
    ####################


    def choose_work_dir(self):
        pass


    # Import selected excel, store columns info and excel path
    # After import, properties list should show sets of column name

    def import_excel(self):
        # Get paths of selecting files
        filenames = QtWidgets.QFileDialog.getOpenFileNames(
            self, self.tr("選取檔案"), ""
            , "All Files (*);;Excel Files (*xlsx);;Excel 97-2003 Files(*xls)"
            , "Excel Files (*xlsx)")

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
            sheetNames = pd.ExcelFile(excelPaths[i]).sheet_names

            if (len(sheetNames) == 1):
                # No sheet name provided, use file name as key
                path = excelPaths[i]
                pos1 = path.rfind("/")
                pos2 = excelPaths[i].rfind(".xls")
                name = path[pos1 + 1 : pos2]
                if name in self.colNamesSet.keys():
                    isDuplicated = True
                else:
                    newKeys.append(name)
                    self.colNamesSet[name] = self.load_excel_columns(excelPaths[i], 0)
            else:
                # Multiple sheets, use (file ： sheet) name as key
                for name in sheetNames:
                    path = excelPaths[i]
                    pos1 = path.rfind("/")
                    pos2 = excelPaths[i].rfind(".xls")
                    keyName = path[pos1 + 1 : pos2] + " ： " + name

                    if keyName in self.colNamesSet.keys():
                        isDuplicated = True
                    else:
                        newKeys.append(keyName)
                        self.colNamesSet[keyName] = self.load_excel_columns(excelPaths[i], name)

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
        print("輸出excel檔案...")

    def add_related_property(self):
        print("新增關聯項目")

    def load_template(self):
        print("讀取樣板...")

    def save_template(self):
        print("儲存樣板...")

    def view_excel(self):
        print("檢視excel...")

    def view_exported_excel(self):
        print("檢視輸出excel")

    def toggle_toolbar(self):
        if (self.toolBar.isVisible()):
            self.toolBar.setVisible(False)
            self.statusBar().showMessage("已關閉工具列", 2000)
        else:
            self.toolBar.setVisible(True)
            self.statusBar().showMessage("已開啟工作列", 2000)

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

    def load_excel_columns(self, _path, _sheetname):

        # Load only first row (column names)
        df = pd.read_excel(_path, _sheetname, nrows=0)
        return df
        
        
        

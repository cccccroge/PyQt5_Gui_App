import sys
from PyQt5 import QtWidgets
import menu
import tool
import status
import central


class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.actions = {}
        self.init_ui()

        global statusBar
        statusBar = self.statusBar()

    def init_ui(self):
        # Sending mainWindow obj to initialize components
        menu.menu(self)
        tool.tool(self)
        status.status(self)
        central.central(self)


    # Action slots
    def choose_work_dir(self):
        print("選擇工作資料夾...")

    def import_excel(self):
        print("匯入excel檔案...")

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
        
        









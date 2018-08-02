import sys
from PyQt5 import QtWidgets
import menu
import tool
import status

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle(self.tr("工研院技轉中心服務程式"))
        self.actions = {}
        self.init_ui()

    def init_ui(self):
        # Sending mainWindow obj to initialize components
        menu.menu(self)
        tool.tool(self)

        global statusBar = self.statusBar()

        s = status.status(self)
        s.show_default()




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
            self.statusBar().showMessage("tool bar disabled", 2000)
        else:
            self.toolBar.setVisible(True)
            self.statusBar().showMessage("tool bar enabled", 2000)

    def toggle_file_manager(self):
        print("開啟/關閉檔案管理面板")
        









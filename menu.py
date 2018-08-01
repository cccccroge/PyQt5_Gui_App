from PyQt5 import QtWidgets
from PyQt5 import QtCore

class menu(QtWidgets.QMenu):
    def __init__(self, menuBar, **kwargs):
        super().__init__(**kwargs)

        menuFile = menuBar.addMenu(self.tr("檔案"))
        actOpenDir = menuFile.addAction(self.tr("選擇工作資料夾"))
        actOpenDir.triggered.connect(lambda: self.choose_work_dir())
        actImportExcel = menuFile.addAction(self.tr("匯入Excel檔案"))
        actImportExcel.triggered.connect(lambda: self.import_excel())
        actExportExcel = menuFile.addAction(self.tr("輸出Excel檔案"))
        actExportExcel.triggered.connect(lambda: self.export_excel())

        menuTool = menuBar.addMenu(self.tr("工具"))
        actAddCompTask = menuTool.addAction(self.tr("新增比對工作項目"))
        actAddCompTask.triggered.connect(lambda: self.add_comparison_task())
        actViewExcel = menuTool.addAction(self.tr("開啟已匯入的Excel檔案"))
        actViewExcel.triggered.connect(lambda: self.view_excel())
        actViewExportedExcel = menuTool.addAction(self.tr("檢視比對序列所輸出的Excel檔案"))
        actViewExportedExcel.triggered.connect(lambda: self.view_exported_excel())

        menuWindow = menuBar.addMenu(self.tr("視窗"))
        actToggleToolbar = menuWindow.addAction(self.tr("顯示/關閉 工具列"))
        actToggleToolbar.triggered.connect(lambda: self.toggle_toolbar())
        actToggleFileExplorer = menuWindow.addAction(self.tr("顯示/關閉 檔案瀏覽面板"))
        actToggleFileExplorer.triggered.connect(lambda: self.toggle_file_explorer())


    # Actions for 檔案
    def choose_work_dir(self):
        print("選擇工作資料夾...")

    def import_excel(self):
        print("匯入excel檔案...")

    def export_excel(self):
        print("輸出excel檔案...")

    # Actions for 工作
    def add_comparison_task(self):
        print("新增比對工作項目")

    def view_excel(self):
        print("檢視excel...")

    def view_exported_excel(self):
        print("檢視輸出excel")

    # Actions for 視窗
    def toggle_toolbar(self):
        print("開啟/關閉工具列")

    def toggle_file_explorer(self):
        print("開啟/關閉檔案檢視面板")

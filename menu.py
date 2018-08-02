from PyQt5 import QtWidgets
from PyQt5 import QtCore

class menu(QtWidgets.QMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # The default menuBar that mainWindow originally preserves
        menuBar = parent.menuBar()
        # Actions dictionary is a field of mainWindow
        actions = parent.actions

        menuFile = menuBar.addMenu(self.tr("檔案"))
        actions["openDir"] = menuFile.addAction(self.tr("選擇工作資料夾"))
        actions["openDir"].triggered.connect(lambda: parent.choose_work_dir())
        actions["importExcel"] = menuFile.addAction(self.tr("匯入Excel檔案"))
        actions["importExcel"].triggered.connect(lambda: parent.import_excel())
        menuFile.addSeparator()
        actions["exportExcel"] = menuFile.addAction(self.tr("輸出Excel檔案"))
        actions["exportExcel"].triggered.connect(lambda: parent.export_excel())

        menuTool = menuBar.addMenu(self.tr("工具"))
        actions["relatedProperty"] = menuTool.addAction(self.tr("新增關聯項目"))
        actions["relatedProperty"].triggered.connect(lambda: parent.add_related_property())
        menuTool.addSeparator()
        actions["loadTemplate"] = menuTool.addAction(self.tr("讀取樣板"))
        actions["loadTemplate"].triggered.connect(lambda: parent.load_template())
        actions["saveTemplate"] = menuTool.addAction(self.tr("儲存樣板"))
        actions["saveTemplate"].triggered.connect(lambda: parent.save_template())
        menuTool.addSeparator()
        actions["viewExcel"] = menuTool.addAction(self.tr("開啟已匯入的Excel檔案"))
        actions["viewExcel"].triggered.connect(lambda: parent.view_excel())
        actions["viewExportedExcel"] = menuTool.addAction(self.tr("預覽輸出Excel檔案"))
        actions["viewExportedExcel"].triggered.connect(lambda: parent.view_exported_excel())

        menuWindow = menuBar.addMenu(self.tr("視窗"))
        actions["toggleToolbar"] = menuWindow.addAction(self.tr("顯示/關閉 工具列"))
        actions["toggleToolbar"].triggered.connect(lambda: parent.toggle_toolbar())
        actions["toggleFileManager"] = menuWindow.addAction(self.tr("顯示/關閉 檔案管理面板"))
        actions["toggleFileManager"].triggered.connect(lambda: parent.toggle_file_manager())




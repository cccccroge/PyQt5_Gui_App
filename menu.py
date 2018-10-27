from PyQt5 import QtWidgets
from PyQt5 import QtCore

import mainWindow
from globalUsed import msgDuration

class menu(QtWidgets.QMenu):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        # The default menuBar that mainWindow originally preserves
        menuBar = parent.menuBar()
        # Actions dictionary is a field of mainWindow
        actions = parent.actions

        menuFile = menuBar.addMenu(self.tr("檔案"))
        actions["openDir"] = menuFile.addAction(self.tr("選擇工作資料夾"))
        actions["openDir"].hovered.connect(lambda: self.on_hovered(parent, 1))
        actions["openDir"].triggered.connect(lambda: parent.choose_work_dir())
        actions["importExcel"] = menuFile.addAction(self.tr("匯入Excel檔案"))
        actions["importExcel"].hovered.connect(lambda: self.on_hovered(parent, 2))
        actions["importExcel"].triggered.connect(lambda: parent.import_excel())
        menuFile.addSeparator()
        actions["exportExcel"] = menuFile.addAction(self.tr("輸出Excel檔案"))
        actions["exportExcel"].hovered.connect(lambda: self.on_hovered(parent, 3))
        actions["exportExcel"].triggered.connect(lambda: parent.export_excel())

        menuTool = menuBar.addMenu(self.tr("工具"))
        actions["relatedProperty"] = menuTool.addAction(self.tr("新增關聯項目"))
        actions["relatedProperty"].hovered.connect(lambda: self.on_hovered(parent, 4))
        actions["relatedProperty"].triggered.connect(lambda: parent.add_related_property())
        menuTool.addSeparator()
        actions["loadTemplate"] = menuTool.addAction(self.tr("讀取樣板"))
        actions["loadTemplate"].hovered.connect(lambda: self.on_hovered(parent, 5))
        actions["loadTemplate"].triggered.connect(lambda: parent.load_template())
        actions["saveTemplate"] = menuTool.addAction(self.tr("儲存樣板"))
        actions["saveTemplate"].hovered.connect(lambda: self.on_hovered(parent, 6))
        actions["saveTemplate"].triggered.connect(lambda: parent.save_template())
        menuTool.addSeparator()
        actions["viewExcel"] = menuTool.addAction(self.tr("開啟已匯入的Excel檔案"))
        actions["viewExcel"].hovered.connect(lambda: self.on_hovered(parent, 7))
        actions["viewExcel"].triggered.connect(lambda: parent.view_excel())
        actions["viewExportedExcel"] = menuTool.addAction(self.tr("預覽輸出Excel檔案"))
        actions["viewExportedExcel"].hovered.connect(lambda: self.on_hovered(parent, 8))
        actions["viewExportedExcel"].triggered.connect(lambda: parent.view_exported_excel())

        menuWindow = menuBar.addMenu(self.tr("視窗"))
        actions["toggleToolbar"] = menuWindow.addAction(self.tr("顯示/關閉 工具列"))
        actions["toggleToolbar"].hovered.connect(lambda: self.on_hovered(parent, 9))
        actions["toggleToolbar"].triggered.connect(lambda: parent.toggle_toolbar())
        actions["toggleMainPanel"] = menuWindow.addAction(self.tr("顯示/關閉 主要工作面板"))
        actions["toggleMainPanel"].hovered.connect(lambda: self.on_hovered(parent, 10))
        actions["toggleMainPanel"].triggered.connect(lambda: parent.toggle_main_panel())


    def on_hovered(self, parent, flag):
        if (flag == 1):
            parent.statusBar().showMessage("選擇資料夾，載入該路徑中所有Excel檔案", msgDuration)
        elif (flag == 2):
            parent.statusBar().showMessage("選擇一個或多個Excel檔案匯入", msgDuration)
        elif (flag == 3):
            parent.statusBar().showMessage("依據目前的關聯項目輸出Excel檔案", msgDuration)
        elif (flag == 4):
            parent.statusBar().showMessage("新增一個空的關聯項目", msgDuration)
        elif (flag == 5):
            parent.statusBar().showMessage("讀取關聯樣板以快速輸出檔案", msgDuration)
        elif (flag == 6):
            parent.statusBar().showMessage("儲存目前的關聯樣板配置", msgDuration)
        elif (flag == 7):
            parent.statusBar().showMessage("選擇並開啟目前匯入Excel檔案", msgDuration)
        elif (flag == 8):
            parent.statusBar().showMessage("預覽目前的輸出Excel檔案", msgDuration)
        elif (flag == 9):
            parent.statusBar().showMessage("顯示或關閉工具列", msgDuration)
        elif (flag == 10):
            parent.statusBar().showMessage("顯示或關閉主要工作面板", msgDuration)





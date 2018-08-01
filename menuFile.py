from PyQt5 import QtWidgets

class menuFile(QtWidgets.QMenu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setTitle("檔案")
        self.addAction("選擇工作資料夾", self.choose_work_dir)
        self.addAction("匯入Excel檔案", self.import_excel)

    def choose_work_dir(self):
        print("已選擇工作資料夾")

    def import_excel(self):
        print("已匯入excel檔案")



#!/usr/bin/python3
from PySide2.QtCore import QDir, Signal, Slot, QFileInfo
from PySide2.QtWidgets import QWidget, QTreeView, QVBoxLayout, QApplication, QPushButton, QGridLayout, QFileDialog, \
    QSplitter
from PySide2.QtGui import QStandardItemModel, QStandardItem

from pics_show import PictureGalaxy


class PlayList(QWidget):
    def __init__(self, view: PictureGalaxy):
        QWidget.__init__(self)
        self.disp_panel = view
        self.disp_panel.pics_consume_out.connect(self.items_consumeout)

        self.items_view = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.items_view.setModel(self.model)
        self.items_view.setHeaderHidden(True)

        layout = QGridLayout(self)
        layout.addWidget(self.items_view, 0, 0, 3, 2)
        self.append = QPushButton("添加", self)
        self.remove = QPushButton("移除", self)
        layout.addWidget(self.append, 3, 1)
        layout.addWidget(self.remove, 3, 0)

        self.append.clicked.connect(self.append_item)

    def items_consumeout(self, last: str):
        print(last)

    def append_item(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选取图片文件夹", QDir.homePath())
        if dir_path == "":
            return

        dir = QDir(dir_path)
        item = QStandardItem(dir.dirName())
        item.setData(dir_path, 10240)

        self.model.appendRow(item)

if __name__ == "__main__":
    app = QApplication()
    split = QSplitter()
    show = PictureGalaxy()
    w = PlayList(show)
    split.addWidget(w)
    split.addWidget(show)
    show.reset_picture_dir(QDir("E:\\.CLOUDSYSTEM\\.HOMES\\18911586235\\来自：百度相册\\贴吧相册"))
    split.show()
    app.exec_()
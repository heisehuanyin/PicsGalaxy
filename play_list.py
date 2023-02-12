#!/usr/bin/python3
from PySide2.QtCore import QDir, Signal, Slot, QFileInfo, QModelIndex, QPoint, QFile, QIODevice, QTextStream
from PySide2.QtWidgets import QWidget, QTreeView, QVBoxLayout, QApplication, QPushButton, QGridLayout, QFileDialog, \
    QSplitter, QListView, QMessageBox, QMenu, QAction
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt

from pics_show import PictureGalaxy


class PlayList(QWidget):
    def __init__(self, view: PictureGalaxy):
        QWidget.__init__(self)
        self.disp_panel = view
        self.disp_panel.pics_consume_out.connect(self.items_consumeout)

        self.items_view = QListView(self)
        self.model = QStandardItemModel(self)
        self.items_view.setModel(self.model)

        layout = QGridLayout(self)
        layout.addWidget(self.items_view, 0, 0, 3, 2)
        self.listload = QPushButton("载入", self)
        self.listsave = QPushButton("保存", self)
        layout.addWidget(self.listload, 3, 1)
        layout.addWidget(self.listsave, 3, 0)

        self.listload.clicked.connect(self.load_list)
        self.listsave.clicked.connect(self.save_list)
        self.items_view.doubleClicked.connect(self.show_contents)

        self.items_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.items_view.customContextMenuRequested.connect(self.show_contexmenu)

    def items_consumeout(self, last: str):
        for idx in range(0, self.model.rowCount()):
            item = self.model.item(idx, 0)
            path = item.data(10240)
            if (path == QFileInfo(last).canonicalPath()) and idx < self.model.rowCount()-1:
                item = self.model.item(idx+1, 0)
                path = item.data(10240)
                self.disp_panel.reset_picture_dir(QDir(path))
                break
        else:
            self.disp_panel.auto_play(False)
            QMessageBox.information(self, "信息提示", "图片播放完毕")

    def load_list(self):
        self.model.clear()
        file_path = QFileDialog.getOpenFileName(self, "打开列表", QDir.homePath())
        if file_path == "":
            return

        symbo = QFile(file_path[0])
        if symbo.open(QIODevice.Text | QIODevice.ReadOnly):
            text_stream = QTextStream(symbo)
            text_stream.setCodec("UTF-8")

            while not text_stream.atEnd():
                line = text_stream.readLine()
                dir = QDir(line)
                if dir.exists():
                    item = QStandardItem(dir.dirName())
                    item.setData(line, 10240)
                    item.setEditable(False)
                    self.model.appendRow(item)

    def save_list(self):
        filepath = QFileDialog.getSaveFileName(self, "保存列表", QDir.homePath())
        if filepath == "":
            return

        filesymbo = QFile(filepath[0])
        if filesymbo.open(QIODevice.Text | QIODevice.WriteOnly):
            text_stream = QTextStream(filesymbo)
            text_stream.setCodec("UTF-8")
            for idx in range(0, self.model.rowCount()):
                item = self.model.item(idx, 0)
                text_stream << item.data(10240) << '\n'
            text_stream.flush()

        pass

    def show_contents(self, index: QModelIndex):
        if not index.isValid():
            return

        curr_item = self.model.itemFromIndex(index)
        path = curr_item.data(10240)
        self.disp_panel.reset_picture_dir(QDir(path))

    def append_item(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选取图片文件夹", QDir.homePath())
        if dir_path == "":
            return

        dir = QDir(dir_path)
        item = QStandardItem(dir.dirName())
        item.setData(dir_path, 10240)
        item.setEditable(False)
        self.model.appendRow(item)

    def remove_item(self):
        curr_idx = self.items_view.currentIndex()
        if not curr_idx.isValid():
            return
        self.disp_panel.auto_play(False)
        self.model.removeRow(curr_idx.row())

    def show_contexmenu(self, point: QPoint):
        menu = QMenu()

        auto_play = QAction("自动播放")
        auto_play.triggered.connect(self.autoplay_start)
        menu.addAction(auto_play)
        menu.addSeparator()

        append = QAction("添加")
        append.triggered.connect(self.append_item)
        menu.addAction(append)

        remove = QAction("删除")
        remove.triggered.connect(self.remove_item)
        menu.addAction(remove)


        idx = self.items_view.indexAt(point)
        if not idx.isValid():
            remove.setEnabled(False)
            auto_play.setEnabled(False)
        menu.exec_(self.mapToGlobal(point))

    def autoplay_start(self):
        index = self.items_view.currentIndex()
        if index.isValid():
            path = index.data(10240)
            self.disp_panel.reset_picture_dir(QDir(path))
            self.disp_panel.auto_play()

if __name__ == "__main__":
    app = QApplication()
    split = QSplitter()
    show = PictureGalaxy()
    w = PlayList(show)
    split.addWidget(w)
    split.addWidget(show)
    show.reset_picture_dir(QDir("E:\\.CLOUDSYSTEM\\.HOMES\\18911586235\\来自：百度相册\\贴吧相册"))
    split.show()
    split.setMinimumSize(600, 400)
    app.exec_()
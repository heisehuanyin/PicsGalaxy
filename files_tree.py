#!/usr/bin/python3

from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QWidget, QTreeView, QApplication, QHBoxLayout, QSplitter, QLabel, QFileIconProvider
from PySide2.QtCore import QDir, QFileInfo, Slot, QModelIndex, Signal
from enum import Enum

from piece_view import PieceView


class NodeType(Enum):
    Driver = 0,
    Dir = 1,
    File = 2,
    PlaceHolder = 3,



class Window(QWidget):
    icons = QFileIconProvider()

    def accept_refresh(self, *args, **dict):
        self.query_child(args[0], 2)

    def query_child(self, mindex: QModelIndex, depth: int):
        if depth == 0:
            return

        item = self.model.itemFromIndex(mindex)
        d = item.data(25509)
        if d == NodeType.Driver or d == NodeType.Dir:
            item.removeRows(0, item.rowCount())
            info = QDir(item.data(25510))
            child = info.entryInfoList(QDir.NoDotAndDotDot|QDir.Filter.Dirs|QDir.Filter.Files)
            it: QFileInfo = None
            for it in child:
                auto_item = QStandardItem(it.fileName())
                auto_item.setIcon(Window.icons.icon(it))
                auto_item.setData(it.absoluteFilePath(), 25510)
                item.appendRow(auto_item)

                if it.isDir():
                    auto_item.setData(NodeType.Dir, 25509)
                    self.query_child(auto_item.index(), depth-1)

        elif d == NodeType.PlaceHolder:
            self.query_child(item.parent().index(), depth -1)

    def show_children(self, *tuple, **dict):
        mindex = tuple[0]
        path = mindex.data(25510)
        self.show_widget.show_contents(QDir(path))

    def __init__(self):
        QWidget.__init__(self)
        self.setMinimumSize(600, 400)

        self.tree = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)

        self.tree.clicked.connect(self.accept_refresh)
        self.tree.clicked.connect(self.show_children)
        self.tree.expanded.connect(self.accept_refresh)

        self.show_widget = PieceView()

        self.split = QSplitter(self)
        self.split.addWidget(self.tree)
        self.split.addWidget(self.show_widget)
        self.split.setSizes([200, 400])

        self.baselayout = QHBoxLayout(self)
        self.baselayout.addWidget(self.split)

        devs = QDir.drives()
        it: QFileInfo = QFileInfo()
        for it in devs:
            info = QStandardItem(it.filePath())
            info.setIcon(Window.icons.icon(it))
            info.setData(NodeType.Driver, 25509)
            info.setData(it.canonicalFilePath(), 25510)
            self.model.appendRow(info)

            self.query_child(info.index(), 2)


app = QApplication()
win = Window()
win.show()
app.exec_()
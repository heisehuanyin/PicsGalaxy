#!/usr/bin/python3

from PySide2.QtWidgets import QWidget, QTreeView, QVBoxLayout, QApplication, QPushButton, QGridLayout
from PySide2.QtGui import QStandardItemModel, QStandardItem


class PlayList(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items_view = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.items_view.setModel(self.model)

        layout = QGridLayout(self)
        layout.addWidget(self.items_view, 0, 0, 3, 2)
        self.append = QPushButton("添加", self)
        self.remove = QPushButton("移除", self)
        layout.addWidget(self.append, 3, 1)
        layout.addWidget(self.remove, 3, 0)

    def append_item(self):


app = QApplication()
w = PlayList()
w.show()
app.exec_()
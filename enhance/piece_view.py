from PySide2.QtCore import QDir, QFile, QFileInfo, QModelIndex, QSize
from PySide2.QtGui import QPainter, QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QWidget, QListView, QStyledItemDelegate, QStyleOptionViewItem, QFileIconProvider


class PieceDelegate(QStyledItemDelegate):
    def __init__(self):
        QStyledItemDelegate.__init__(self)
        pass

    def sizeHint(self, option:QStyleOptionViewItem, QModelIndex) -> QSize:
        return QSize(60,100)


    def paint(self, painter:QPainter, option:QStyleOptionViewItem, index:QModelIndex) -> None:
        QStyledItemDelegate.paint(self, painter, option, index)
        pass


class PieceView(QListView):
    icons = QFileIconProvider()

    def __init__(self):
        QListView.__init__(self)
        self.setItemDelegate(PieceDelegate())
        self.datas = QStandardItemModel()
        self.setModel(self.datas)
        self.setViewMode(QListView.ViewMode.IconMode)

    def show_contents(self, con: QDir):
        self.datas.clear()

        items = con.entryInfoList(QDir.Files|QDir.Dirs|QDir.NoDotAndDotDot)
        it: QFileInfo = None
        for it in items:
            auto_item = QStandardItem(it.fileName())
            auto_item.setIcon(PieceView.icons.icon(it))
            auto_item.setData(it.canonicalPath(), 65535)
            auto_item.setEditable(False)
            self.datas.appendRow(auto_item)



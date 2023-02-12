from typing import List, Dict

from PySide2.QtCore import QDir, QFileInfo, QRect, QTimer, Signal, Slot, QEvent
from PySide2.QtGui import QStandardItemModel, QPaintEvent, Qt, QStandardItem, QMouseEvent, QPixmap, QPainter, \
    QColor, QPen, QBrush
from PySide2.QtWidgets import QApplication, QWidget


class PictureGalaxy(QWidget):
    pics_consume_out = Signal(str)

    def __init__(self):
        QWidget.__init__(self)
        self.img_types: List[str] = ["*.jpeg", "*.jpg", "*.png", "*.bmp"]
        self.datas = QStandardItemModel()
        self.pics_cache: Dict[str, QPixmap] = {}
        self.index = 0
        self.area = None
        self.setMouseTracking(True)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.accept_play_trigger)

    def accept_play_trigger(self):
        if self.index == self.datas.rowCount() - 1:
            curr_item: QStandardItem = self.datas.item(self.index, 0)
            self.pics_consume_out.emit(curr_item.data(65535))

        self.index = min(self.index + 1, self.datas.rowCount() - 1)
        self.update()
        pass

    def auto_play(self, enable:bool =True, msecs: int = 2000):
        if enable:
            if self.timer.isActive():
                self.timer.stop()

            self.timer.setInterval(msecs)
            self.timer.start()
        else:
            self.timer.stop()

    def reset_picture_dir(self, conn: QDir):
        self.datas.clear()
        self.pics_cache = {}
        items = conn.entryInfoList(self.img_types, QDir.Files, QDir.Name)
        self.index = 0

        it: QFileInfo = None
        for it in items:
            auto_item = QStandardItem(it.fileName())
            real_path = it.canonicalFilePath()
            auto_item.setData(real_path, 65535)
            self.datas.appendRow(auto_item)

        self.update()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        vcube = self.size()
        if event.pos().x() < vcube.width() * 0.1:
            self.area = QRect(0, 0, vcube.width() * 0.1, vcube.height())
        elif event.pos().x() > vcube.width() * 0.9:
            self.area = QRect(vcube.width() * 0.9, 0, vcube.width() * 0.1, vcube.height())
        elif self.area != None:
            self.area = None
        self.update()

    def leaveEvent(self, event:QEvent) -> None:
        self.area = None
        self.update()

    def mousePressEvent(self, event:QMouseEvent) -> None:
        vcube = self.size()
        if event.pos().x() < vcube.width() * 0.1:
            self.index = max(self.index - 1, 0)
            self.update()
        elif event.pos().x() > vcube.width() * 0.9:
            if self.index == self.datas.rowCount() - 1:
                curr_item: QStandardItem = self.datas.item(self.index, 0)
                self.pics_consume_out.emit(curr_item.data(65535))

            self.index = min(self.index + 1, self.datas.rowCount() - 1)
            self.update()
        self.setWindowTitle(self.datas.item(self.index).data(65535))

    def paintEvent(self, event: QPaintEvent) -> None:
        QWidget.paintEvent(self, event)

        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        if self.datas.rowCount() == 0:
            return

        curr_item: QStandardItem = self.datas.item(self.index, 0)
        path = curr_item.data(65535)
        if path not in self.pics_cache:
            self.pics_cache[path] = QPixmap(path)

        pixmap = self.pics_cache[path]
        target_rect = self.rect()
        src_rect = pixmap.rect()
        frame_rect = self.rect()
        if target_rect.width()/target_rect.height() > src_rect.width()/src_rect.height():
            target_rect.setWidth(target_rect.height()*src_rect.width()/src_rect.height())
            target_rect.moveLeft((frame_rect.width() - target_rect.width()) / 2)
        else:
            target_rect.setHeight(target_rect.width()*src_rect.height()/src_rect.width())
            target_rect.moveTop((frame_rect.height() - target_rect.height()) / 2)


        painter.drawPixmap(target_rect, pixmap)
        painter.setPen(QPen(QBrush(Qt.white), 1))
        painter.drawRect(target_rect)

        if self.area is not None:
            painter.fillRect(self.area, QColor.fromRgb(255, 255, 255, 80))
        pass

@Slot(str)
def xprint(str):
    print(str)

if __name__ == "__main__":
    app = QApplication()
    w = PictureGalaxy()
    w.show()
    w.reset_picture_dir(QDir("""E:\\.CLOUDSYSTEM\\.HOMES\\18911586235\\来自：百度相册\\贴吧相册"""))
    w.auto_play(True, 5000)
    w.pics_consume_out.connect(xprint)
    app.exec_()

from PySide2.QtCore import QDir
from PySide2.QtWidgets import QApplication, QSplitter, QMainWindow

from PicsShow import PictureGalaxy
from PlayList import PlayList

if __name__ == "__main__":
    app = QApplication()
    win = QMainWindow()
    win.setMinimumSize(600, 400)

    split = QSplitter()
    win.setCentralWidget(split)

    show = PictureGalaxy()
    w = PlayList(show)
    split.addWidget(w)
    split.addWidget(show)

    win.show()
    app.exec_()
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
    list = PlayList(show)
    split.addWidget(list)
    split.addWidget(show)

    def show_title(title:str):
        win.setWindowTitle(title)

    show.current_picture_changed.connect(show_title)

    win.show()
    app.exec_()
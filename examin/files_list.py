from PySide2.QtCore import QFileInfo, QDir, QFile
from PySide2.QtWidgets import QWidget


info = QFileInfo("C:\Qt")
dir = QDir(info.absoluteFilePath())

it: QFileInfo = None
for it in dir.entryInfoList(QDir.Filter.Dirs|QDir.Filter.Files):
    print(it.absoluteFilePath())
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from pythonGUI import follow_stream
import sys

class FollowStreamWindow(follow_stream.Ui_FollowStreamWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formatComboBox.clear()
        self.formatComboBox.addItems(["ASCII", "Hex Dump", "UTF-8", "UTF-16", "YAML"])


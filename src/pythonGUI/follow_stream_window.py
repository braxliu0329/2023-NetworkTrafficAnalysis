from PyQt5.QtWidgets import *
from pythonGUI import follow_stream
import pyshark
import re
import os

class FollowStreamWindow(follow_stream.Ui_FollowStreamWindow, QMainWindow):
    def __init__(self, file_name, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.file_name = file_name
        self.setupUi(self)
        self.formatComboBox.clear()
        self.formatComboBox.addItems(["ASCII", "Hex", "UTF-8", "UTF-16", "YAML"])
        self.set_stream()
        
    def set_stream(self):
        stream_index = self.streamNumberSpinBox.value()
        cap = pyshark.FileCapture(self.file_name, display_filter=f"tcp.stream eq {stream_index}")
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        conversation = ""
        while True:
            try:
                pkt = cap.next()
            except StopIteration:
                break
            try:
                conversation += ansi_escape.sub('',str(pkt.http).replace('\\n','').replace('\\r',''))
            except AttributeError:
                pass
        self.streamViewer.setText(conversation)

    def closeEvent(self, event):
        os.remove(self.file_name)
        self.mainWindow.actionFollowStream.setDisabled(False)
        event.accept()



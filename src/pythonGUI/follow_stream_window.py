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

        stream_index = []
        self.streams = {}
        self.cap = pyshark.FileCapture(self.file_name)
        for pkt in self.cap:
            try:
                stream_index.append(pkt.tcp.stream)
            except:
                pass
        if len(stream_index) == 0:
            max_index = 0
        else:
            max_index = int(max(stream_index)) + 1
        components = 1
        client = ""
        server = ""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        for stream in range(0, max_index):
            for pkt in self.cap:
                try:
                    if int(pkt.tcp.stream) == stream:
                        if components % 2 == 1:
                            client += ansi_escape.sub('',str(pkt.http).replace('\\n','').replace('\\r',''))
                        if components % 2 == 0:
                            server += ansi_escape.sub('',str(pkt.http).replace('\\n','').replace('\\r',''))
                            self.streams[stream] = (client,server)
                        components += 1
                except:
                    pass
 
        self.streamNumberSpinBox.setMaximum(max_index - 1)

        self.closePushButton.clicked.connect(self.close)
        self.streamNumberSpinBox.valueChanged.connect(self.set_stream)
        self.formatComboBox.currentTextChanged.connect(self.set_stream)

        self.formatComboBox.clear()
        self.formatComboBox.addItems(["ASCII", "Hex", "UTF-8", "UTF-16", "YAML"])
        self.set_stream()
    
    def set_stream(self):
        stream_index = self.streamNumberSpinBox.value()
        self.streamViewer.clear()
        self.streamViewer.append(self.streams[stream_index][0])
        self.streamViewer.append(self.streams[stream_index][1])

    def closeEvent(self, event):
        os.remove(self.file_name)
        self.mainWindow.actionFollowStream.setDisabled(False)
        event.accept()



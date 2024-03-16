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
        self.streams = {"client_data": {}, "server_data": {}}
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
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        for stream in range(0, max_index):
            client = ''
            server = ''
            for pkt in self.cap:
                try:
                    if int(pkt.tcp.stream) == stream:
                            stream_data = ansi_escape.sub('',str(pkt.http).replace('\\n','').replace('\\r',''))
                            if hasattr(pkt.http, "request"):
                                client += stream_data
                            else:
                                server += stream_data
                except:
                    pass
            self.streams["client_data"][stream] = client
            self.streams["server_data"][stream] = server
        self.streamNumberSpinBox.setMaximum(max_index - 1)

        self.closePushButton.clicked.connect(self.close)
        self.streamNumberSpinBox.valueChanged.connect(self.set_stream)
        self.formatComboBox.currentTextChanged.connect(self.set_stream)

        self.formatComboBox.clear()
        self.formatComboBox.addItems(["ASCII", "Hex", "UTF-8", "UTF-16", "YAML"])
        self.conversationComboBox.clear()
        self.conversationComboBox.addItems(["Entire conversation", "Client to server", "Server to client"])

        self.set_stream()
    
    def set_stream(self):
        stream_index = self.streamNumberSpinBox.value()
        self.streamViewer.clear()
        self.streamViewer.append(self.streams["client_data"][stream_index])
        self.streamViewer.append(self.streams["server_data"][stream_index])


    def closeEvent(self, event):
        os.remove(self.file_name)
        self.mainWindow.actionFollowStream.setDisabled(False)
        event.accept()



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

        self.formatComboBox.clear()
        self.formatComboBox.addItems(["UTF-8", "UTF-16", "ASCII", "Hex", "YAML" ])
        self.conversationComboBox.clear()
        self.conversationComboBox.addItems(["Entire conversation", "Client to server", "Server to client"])

        self.closePushButton.clicked.connect(self.close)
        self.streamNumberSpinBox.valueChanged.connect(self.set_stream)
        self.formatComboBox.currentTextChanged.connect(self.set_stream)
        self.conversationComboBox.currentTextChanged.connect(self.set_stream)

        self.set_stream()
    
    def set_stream(self):
        stream_index = self.streamNumberSpinBox.value()
        self.streamViewer.clear()
        conversation = self.conversationComboBox.currentText()
        format = self.formatComboBox.currentText()
        client = self.streams["client_data"][stream_index]
        server = self.streams["server_data"][stream_index]
        if format == "utf-16":
            client = client.encode("utf-16")
            server = server.encode("utf-16")
        if format == "ASCII":
            client = client.encode("ascii", errors="itnore").decode("ascii")
            server = server.encode("ascii", errors="itnore").decode("ascii")
        if format == "Hex":
            client = client.encode("utf8").hex()
            server = server.encode("utf-8").hex()
        client = "<html><body style='white-space: pre'>{}</body></html>".format(
            '<span style="background-color: #ED6769;">{}</span>'.format(
                client.replace('\n', '<br>')))
        server = "<html><body style='white-space: pre'>{}</body></html>".format(
            '<span style="background-color: #6769ED;">{}</span>'.format(
                server.replace('\n', '<br>')
            )
        )
        if conversation == "Entire conversation" or conversation == "Client to server":
            self.streamViewer.append(client)
        if conversation == "Entire conversation" or conversation == "Server to client":
            self.streamViewer.append(server)


    def closeEvent(self, event):
        os.remove(self.file_name)
        self.mainWindow.actionFollowStream.setDisabled(False)
        event.accept()



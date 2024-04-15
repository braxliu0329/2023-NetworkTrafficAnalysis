
import io
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from pythonGUI import follow_stream
import os
# PyYaml does not preserve the formatting, whereas ruamel does
from ruamel.yaml import YAML
import tshark_wrapper.tshark as tshark
import re


class FollowStreamWindow(follow_stream.Ui_FollowStreamWindow, QMainWindow):
    def __init__(self, file_name, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.file_name = file_name
        self.setupUi(self)

        self.peers = {}
        self.packet_yaml = {}
        self.streams = {"ascii": {}, "utf-8": {}, "hex": {}, "raw": {}, "ebcdic": {}, "yaml": {}}
        self.formatComboBox.clear()
        self.formatComboBox.addItems(
            ["UTF-8", "ASCII", "Hex", "Raw", "EBCDIC", "YAML"])
        self.conversationComboBox.clear()
        self.conversationComboBox.addItems(
            ["Entire conversation", "Client to server", "Server to client"])

        self.closePushButton.clicked.connect(self.close)
        self.streamNumberSpinBox.valueChanged.connect(self.set_stream)
        self.formatComboBox.currentTextChanged.connect(self.set_stream)
        self.conversationComboBox.currentTextChanged.connect(self.set_stream)
        self.printPushButton.clicked.connect(self.print_conversation)
        self.savePushButton.clicked.connect(self.save_conversation)

        self.set_stream()

    def load_tcp_stream(self, stream_format, stream):
        if stream not in self.streams[stream_format]:
            self.streams[stream_format][stream] = tshark.tcp_stream(self.file_name, stream_format, stream)
        
 
    def set_stream(self):
        self.streamViewer.clear()
        stream = self.streamNumberSpinBox.value()
        conversation = self.conversationComboBox.currentText()
        stream_format = self.formatComboBox.currentText().lower()
        print(stream_format)

        if stream_format == "yaml":
            self.load_tcp_stream(stream_format, stream)
            loaded_stream = self.streams[stream_format][stream]
            self.streamViewer.setText(loaded_stream)
        else:
            self.load_tcp_stream(stream_format, stream)
            loaded_stream = self.streams[stream_format][stream]
            if conversation == "Client to server" or conversation == "Entire conversation":
                self.streamViewer.setTextBackgroundColor(QColor(105, 103, 237))
                client_to_server = loaded_stream.split('\t', maxsplit=1)[0]
                self.streamViewer.append(client_to_server)
            if conversation == "Server to client" or conversation == "Entire conversation":
                self.streamViewer.setTextBackgroundColor(QColor(237, 103, 105))
                server_to_client = loaded_stream.split('\t', maxsplit=1)[1]
                self.streamViewer.append(server_to_client)
            
            
            
            
            
            
            

    def print_conversation(self):
        print(self.streamViewer.toPlainText())

    def save_conversation(self):
        stream_format = self.formatComboBox.currentText()
        stream_index = self.streamNumberSpinBox.value()
        conversation = self.streamViewer.toPlainText()
        name = self.file_name.split('.')[0] + "TCPIndex" + str(stream_index)
        if stream_format == "YAML":
            name = name + ".yaml"
            with open(name, "w+") as f:
                f.write(conversation)
        elif stream_format == "UTF-8" or stream_format == "ASCII":
            name = name + ".txt"
            with open(name, "w+") as f:
                f.write(conversation)
        else:
            name = name + ".bin"
            with open(name, "wb+") as f:
                f.write(bytearray.fromhex(conversation))

    def closeEvent(self, event):
        os.remove(self.file_name)
        self.mainWindow.actionFollowStream.setDisabled(False)
        event.accept()

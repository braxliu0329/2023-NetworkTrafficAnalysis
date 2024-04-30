from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from pythonGUI import follow_stream
import os
import tshark_wrapper.tshark as tshark


class FollowStreamWindow(follow_stream.Ui_FollowStreamWindow, QMainWindow):
    def __init__(self, file_name, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.file_name = file_name
        self.setupUi(self)

        #Store each stream for each format in a separate dict for quick access
        #Each stream will contain a tuple of lists of strings
        #The left entry contains all requests in that stream
        #The right entry contains all responses in that stream
        #This does not apply for non ASCII/UTF-8 formats
        #Raw data uses the streams from "ascii" and encodes the bytes as hex
        self.streams = {"ascii": {}, "utf-8": {}, "yaml": {}}
        self.formatComboBox.clear()
        self.formatComboBox.addItems(
            ["UTF-8", "ASCII", "Raw", "YAML"])
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
        if stream_format == "raw":
            stream_format == "ascii"
        if stream not in self.streams[stream_format]:
            if stream_format != "yaml":
                loaded_stream = tshark.tcp_stream(self.file_name, stream_format, stream)
                if loaded_stream is None:
                    return 1
                loaded_stream = tshark.split_stream(loaded_stream)
                if loaded_stream is None:
                    if stream == 0:
                        self.streamNumberSpinBox.setMaximum(stream)
                    else:
                        self.streamNumberSpinBox.setMaximum(stream - 1)
                self.streams[stream_format][stream] = loaded_stream
            else:
                loaded_stream = tshark.tcp_stream(self.file_name, stream_format, stream)
                self.streams[stream_format][stream] = loaded_stream
        return 0
    
    def set_stream(self):
        self.streamViewer.clear()
        stream = self.streamNumberSpinBox.value()
        conversation = self.conversationComboBox.currentText()
        stream_format = self.formatComboBox.currentText().lower()
        #YAML format displays content differently to the others.
        #Other formats use a tab character to separate c2s and s2c.
        #YAML requires some extra logic, which involves identifying the c2s peer, and the s2c peer
        #then color coding the respective peers.
        #Entries are wrapped in a html tag to render the background.
        #The HTML tags couldn't be used in the other formats since the ASCII and UTF-8 versions
        #contain XML. Having XML wrapped in a HTML tag renders the XML as an actual webpage.
        if stream_format == "yaml":
            if self.load_tcp_stream(stream_format, stream) == 1:
                return
            loaded_stream = self.streams[stream_format][stream]
            color_coded_yaml = "<html><body style='white-space: pre'>Peers:<br>"
            for line in loaded_stream.split("-"):
                if "peer" in line and "peers" not in line:
                    if (conversation == "Entire conversation" or conversation == "Client to server") and "peer: 0" in line:
                        color_coded_yaml += f'<span style="background-color: #ED6769">-{line}</span>'
                    if (conversation == "Entire conversation" or conversation == "Server to client") and "peer: 1" in line:
                        color_coded_yaml += f'<span style="background-color: #6769ED">-{line}</span>'
                
            color_coded_yaml += "</body></html>"
            self.streamViewer.setText(color_coded_yaml)
        else:
            if stream_format == "raw":
                if self.load_tcp_stream("ascii", stream) == 1:
                    return
                loaded_stream = self.streams["ascii"][stream]
            else:
                if self.load_tcp_stream(stream_format, stream) == 1:
                    return
                loaded_stream = self.streams[stream_format][stream]
            if loaded_stream is None:
                return  
            for i in range(len(loaded_stream[0])):
                if conversation == "Client to server" or conversation == "Entire conversation":
                    self.streamViewer.setTextBackgroundColor(QColor(105, 103, 237))
                    if stream_format == "raw":
                        self.streamViewer.append(loaded_stream[0][i].encode("ascii").hex())
                    else:
                        self.streamViewer.append(loaded_stream[0][i])
                if conversation == "Server to client" or conversation == "Entire conversation":
                    self.streamViewer.setTextBackgroundColor(QColor(237, 103, 105))
                    if stream_format == "raw":
                        self.streamViewer.append(loaded_stream[1][i].encode("ascii").hex())
                    else:
                        self.streamViewer.append(loaded_stream[1][i])
            
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
        event.accept()

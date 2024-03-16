import base64
from PyQt5.QtWidgets import *
import yaml
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
        self.peers = {}
        self.packet_yaml = []
        self.streams = {"client_data": {}, "server_data": {}}
        self.cap = pyshark.FileCapture(self.file_name)
        for pkt in self.cap:
            try:
                stream_index.append(pkt.tcp.stream)
            except:
                pass
            try:
                src_ip = str(pkt.ip.src)
                src_port = int(pkt.tcp.srcport)
                dst_ip = str(pkt.ip.dst)
                dst_port = int(pkt.tcp.dstport)
                data = pkt.tcp.payload
                if (src_ip, src_port) not in self.peers.values():
                    peer_id = len(self.peers)
                    self.peers[peer_id] = {'host': src_ip, 'port': src_port}
                if (dst_ip, dst_port) not in self.peers.values():
                    peer_id = len(self.peers)
                    self.peers[peer_id] = {'host': dst_ip, 'port': dst_port}
                try:
                    peer_id = next(key for key, value in self.peers.items() if value == (src_ip, src_port))
                except StopIteration:
                    pass
                packet_info = {
                    'packet': int(pkt.number),
                    'peer': peer_id,
                    'index': 0,  # Assuming index is always 0 for simplicity
                    'timestamp': float(pkt.frame_info.time_epoch),
                    'data': base64.b64encode(bytes.fromhex(data.replace(':', ''))).decode()
                }
                self.packet_yaml.append(packet_info)
            except AttributeError:
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
        self.printPushButton.clicked.connect(self.print_conversation)

        self.set_stream()
    
    def set_stream(self):
        yaml_stream = {'peers': [{'peer': key, 'host': value['host'], 'port': value['port']} for key, value in self.peers.items()], 'packets': self.packet_yaml}
        print(yaml.dump(yaml_stream["peers"], default_flow_style=False))
        with open("stream.yaml", "w+") as f:
            yaml_stream = yaml.safe_dump(yaml_stream, f, default_flow_style=False)
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

    def print_conversation(self):
        print(self.streamViewer.toPlainText())


    def closeEvent(self, event):
        os.remove(self.file_name)
        self.mainWindow.actionFollowStream.setDisabled(False)
        event.accept()



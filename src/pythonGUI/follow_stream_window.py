import base64
import io
from PyQt5.QtWidgets import *
from pythonGUI import follow_stream
import pyshark
import re
import os
import sys
# PyYaml does not preserve the formatting, whereas ruamel does
from ruamel.yaml import YAML
class FollowStreamWindow(follow_stream.Ui_FollowStreamWindow, QMainWindow):
    def __init__(self, file_name, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.file_name = file_name
        self.setupUi(self)

        stream_index = []
        self.peers = {}
        self.packet_yaml = {}
        self.streams = {"client_data": {}, "server_data": {}}
        self.cap = pyshark.FileCapture(self.file_name)
        for pkt in self.cap:
            try:
                stream = pkt.tcp.stream
                stream_index.append(stream)
                src_ip = str(pkt.ip.src)
                src_port = int(pkt.tcp.srcport)
                dst_ip = str(pkt.ip.dst)
                dst_port = int(pkt.tcp.dstport)
                data = pkt.tcp.payload
                if (src_ip, src_port) not in self.peers.values():
                    peer_id = len(self.peers)
                    self.peers[peer_id] = {'host': src_ip, 'port': src_port}
                    self.peers[peer_id]["stream"] = int(stream)
                if (dst_ip, dst_port) not in self.peers.values():
                    peer_id = len(self.peers)
                    self.peers[peer_id] = {'host': dst_ip, 'port': dst_port}
                    self.peers[peer_id]["stream"] = int(stream)
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
                if int(stream) in self.packet_yaml:
                    self.packet_yaml[int(stream)].append(packet_info)
                else:
                    self.packet_yaml[int(stream)] = [packet_info]
            except AttributeError:
                pass
        if len(stream_index) == 0:
            self.max_index = 0
        else:
            self.max_index = int(max(stream_index)) + 1
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        for stream in range(0, self.max_index):
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
        self.streamNumberSpinBox.setMaximum(self.max_index - 1)

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
        
    def make_yaml_stream(self):
        yaml_stream = {}
        for peer in self.peers.keys():
            for stream in range(0,self.max_index):
                if self.peers[peer]["stream"] == stream:
                    peer_info = {
                        'peer': peer,
                        'host': self.peers[peer]["host"],
                        'port': self.peers[peer]["port"]
                    }
                    if stream in yaml_stream:
                        yaml_stream[stream].append(peer_info)
                    else:
                        yaml_stream[stream] = [peer_info]
                    break
        return yaml_stream

    def set_stream(self):
        stream_index = self.streamNumberSpinBox.value()
        self.streamViewer.clear()
        conversation = self.conversationComboBox.currentText()
        stream_format = self.formatComboBox.currentText()
        if stream_format == "YAML":
            yaml_peer = self.make_yaml_stream()[stream_index]
            yaml_packets = self.packet_yaml[stream_index]
            yaml_stream = {"peers": yaml_peer, "packets": yaml_packets}
            yaml = YAML()
            yaml.default_flow_style = False
            buf = io.BytesIO()
            yaml.dump(yaml_stream, buf)
            self.streamViewer.setText(buf.getvalue().decode('utf-8'))
        else:    
            client = self.streams["client_data"][stream_index]
            server = self.streams["server_data"][stream_index]
            if stream_format == "utf-16":
                client = client.encode("utf-16")
                server = server.encode("utf-16")
            if stream_format == "ASCII":
                client = client.encode("ascii", errors="itnore").decode("ascii")
                server = server.encode("ascii", errors="itnore").decode("ascii")
            if stream_format == "Hex":
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



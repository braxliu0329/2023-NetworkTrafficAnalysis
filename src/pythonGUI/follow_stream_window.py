import base64
import io
from PyQt5.QtWidgets import *
from pythonGUI import follow_stream
import pyshark
import re
import os
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
        # Go through the captured packets, and track the protocol stream
        for pkt in self.cap:
            try:
                stream = pkt.tcp.stream
                stream_index.append(stream)
                src_ip = str(pkt.ip.src)
                src_port = int(pkt.tcp.srcport)
                dst_ip = str(pkt.ip.dst)
                dst_port = int(pkt.tcp.dstport)
                data = pkt.tcp.payload

                # Conversation in YAML show peers in a network, and the packets communicated between them
                self.update_peer(int(stream), src_ip, src_port)
                self.update_peer(int(stream), dst_ip, dst_port)
                packet_info = {
                    'packet': int(pkt.number),
                    'peer': self.get_peer_id(int(stream), src_ip, src_port),
                    'index': 0,  
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
            max_index = 0
        else:
            max_index = int(max(stream_index)) + 1
        # Make a regex for ANSI escape characters and remove them from the HTTP field
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

    def update_peer(self, stream, ip, port):
        if stream not in self.peers:
            self.peers[stream] = {}
        found_peer = False
        for peer_id, peer_info in self.peers[stream].items():
            if peer_info['host'] == ip and peer_info['port'] == port:
                found_peer = True
                break
        if not found_peer:
            peer_id = len(self.peers[stream])
            self.peers[stream][peer_id] = {
                'host': ip,
                'port': port
            }

    def get_peer_id(self, stream, ip, port):
        for peer_id, peer_info in self.peers[stream].items():
            if peer_info['host'] == ip and peer_info['port'] == port:
                return peer_id
        return None
        
    def make_yaml_stream(self):
        yaml_peers = {}
        for stream, peers_info in self.peers.items():
            yaml_peers[stream] = [{'peer': peer_id, 'host': info['host'], 'port': info['port']} for peer_id, info in peers_info.items()]
        print(yaml_peers)
        return yaml_peers

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



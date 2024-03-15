from PyQt5.QtWidgets import *
from pythonGUI import follow_stream
import pyshark

class FollowStreamWindow(follow_stream.Ui_FollowStreamWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formatComboBox.clear()
        self.formatComboBox.addItems(["ASCII", "Hex", "UTF-8", "UTF-16", "YAML"])
        self.set_stream()
        

    def set_stream(self):
        stream_index = self.streamNumberSpinBox.value()
        cap = pyshark.FileCapture("http.cap", display_filter=f"tcp.stream eq {stream_index}")
        conversation = ""
        while True:
            try:
                pkt = cap.next()
            except StopIteration:
                break
            try:
                conversation += str(pkt.http).replace('\\n','').replace('\\r','')
            except AttributeError:
                pass
        self.streamViewer.setText(conversation)



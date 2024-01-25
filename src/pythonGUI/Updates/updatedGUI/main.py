import os.path

from PyQt5.Qt import Qt, QCompleter
from PyQt5.QtCore import QSortFilterProxyModel, QUrl
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QTreeWidgetItem, QMenu, QAction
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QComboBox
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether
from PyQt5.QtGui import QDesktopServices
import webbrowser
import sys
sys.path.append("src/")
from mainWindow import Ui_MainWindow
from packetDetails import Ui_PacketDetails
from pythonGUI.capture_analysis import GUI_actions, attack_detection
import rc_icons

def hex_packet_data(packet_data):
    result = []
    digits = 4 if isinstance(packet_data, str) else 2

    for i in range(0, len(packet_data), 16):
        data = packet_data[i: i + 16]
        hexa = ' '.join([hex(x)[2:].upper().zfill(digits) for x in data])
        text = ' '.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in data])
        result.append("{0:04X}".format(i) + ' --- ' + hexa.ljust(16 * (digits + 1)) + ' --- ' + "{0}".format(text))

    return ' --- '.join(result)

class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.data_box_menu = QMenu(self)

        self.detect = None
        self.cwd = None
        self.stopped_capture = False
        self.capture_thread = None
        self.packet_number = 1
        # creates GUI_actions object
        self.GUI_actions = GUI_actions.GUIActions()
        self.setupUi(self)
        self.showMaximized()
        self.flaggedIPs = []
        self.show_in_hex = None
        self.show_in_bin = None

        self.startButton.clicked.connect(self.start_capture)
        self.stopButton.clicked.connect(self.stop_capture)

    def start_capture(self):
        self.open_window()
        self.startButton.setEnabled(False)
        self.pauseButton.setEnabled(True)
        self.stopButton.setEnabled(True)

        # creates a thread to run simultaneously so the user can still interact with GUI
        self.capture_thread = threading.Thread(target=self.start_capture_thread)
        # starts running the thread
        self.capture_thread.start()

    def open_window(self):
        self.window = QMainWindow()
        self.ui = Ui_PacketDetails()
        self.ui.setupUi(self.window)
        self.window.show()

    def stop_capture(self):
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)

        self.stopped_capture = True
        self.packetTable.setRowCount(0)
        self.GUI_actions.start_sniffer(False, mainWindow)
        self.packet_number = 1

        self.GUI_actions.sniffer.reset()




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())
       




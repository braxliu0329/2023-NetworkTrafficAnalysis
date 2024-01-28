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

        #set packet table
        self.packetTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.packetTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.packetTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.packetTable.verticalHeader().setVisible(False)
        self.packetTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.packetTable.cellClicked.connect(self.handle_clicked_row)
        self.packetTable.cellClicked.connect(self.get_select_packet)
        self.packetTable.cellClicked.connect(self.get_current_list_row)
        self.packetTable.cellDoubleClicked.connect(self.handle_double_clicked_row)

        #set the help menu
        self.actionUse_Guide.triggered.connect(self.use_guide_operation)    
        #start button pressed
        self.startButton.clicked.connect(self.start_capture)
        #stop button pressed
        self.stopButton.clicked.connect(self.stop_capture)

    def get_select_packet(self, row):
        pass

    def handle_clicked_row(self, row):
        selected_packet, details = self.get_select_packet(row)
    
    def get_current_list_row(self):
        pass

    def handle_double_clicked_row(self, row):
        pass
        
    def use_guide_operation(self):
        webbrowser.open_new_tab('https://ubiquitous-sniffle-y217w7w.pages.github.io/#/')

    def start_capture_thread(self):
        self.stopped_capture = False
        self.GUI_actions.sniffer.set_sniff_amount(self)

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
        self.packet_window = PacketDetailsWindow(self)
        self.ui = Ui_PacketDetails()
        self.ui.setupUi(self.window)
        self.packet_window.show()

    def stop_capture(self):
        self.startButton.setEnabled(True)
        self.pauseButton.setEnabled(False)
        self.stopButton.setEnabled(False)

        self.stopped_capture = True
        self.packetTable.setRowCount(0)
        self.GUI_actions.start_sniffer(False, mainWindow)
        self.packet_number = 1

        self.GUI_actions.sniffer.reset()

    class TableItemInt(QTableWidgetItem):
        # less than initializer that allows two items to be compared.
        def __lt__(self, other):
            return int(self.text()) < int(other.text())

    def display_packet(self, packet):
        row_number = self.packetTable.rowCount()
        self.packetTable.inserRow(row_number)
        packet_number_item = self.TableItemInt(str(self.packet_number))
        self.packetTable.setItem(row_number, 0, packet_number_item)


class PacketDetailsWindow(QMainWindow):
    def __init__(self, mainWindow):
        super(PacketDetailsWindow, self).__init__()
        self.mainWindow = mainWindow
    
    def update_packet_details(self, packet):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())
       




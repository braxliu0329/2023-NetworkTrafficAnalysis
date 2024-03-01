from dataclasses import dataclass
import os.path
import sys
import hashlib

from PyQt5.Qt import Qt, QCompleter
from PyQt5.QtCore import QSortFilterProxyModel, pyqtSignal
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QTreeWidgetItem, QMenu, QAction
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QComboBox
from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.inet6 import IPv6
from scapy.layers.l2 import ARP, Ether
from PyQt5.QtGui import QDesktopServices
import webbrowser

from pythonGUI.capture_analysis import plotting
from pythonGUI import subWindow, window, attack_analysis_action, message

from pythonGUI.capture_analysis import GUI_actions, attack_detection

import pythonGUI.rc_icons as rc_icons

# Turns the packet data into a hex string
def hex_packet_data(packet_data):
    result = []
    digits = 4 if isinstance(packet_data, str) else 2
    # loops through the length of packet data
    for i in range(0, len(packet_data), 16):
        # gets the data for the current packet in a 16 byte chunk
        data = packet_data[i: i + 16]
        hexa = ' '.join([hex(x)[2:].upper().zfill(digits) for x in data])
        text = ' '.join([chr(x) if 0x20 <= x < 0x7F else '.' for x in data])
        result.append("{0:04X}".format(i) + ' --- ' + hexa.ljust(16 * (digits + 1)) + ' --- ' + "{0}".format(text))

    return ' --- '.join(result)

# define the window class that inherits from the GUI window class and the main window class
class Window(window.Ui_MainWindow, QMainWindow):

    permission_allowed = pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()

        self.data_box_menu = QMenu(self)

        self.detect = None
        self.cwd = None
        self.stopped_capture = False
        self.packet_number = 1
        # creates GUI_actions object
        self.GUI_actions = GUI_actions.GUIActions()
        self.setupUi(self)
        self.showMaximized()
        self.flaggedIPs = []
        self.show_in_hex = None
        self.show_in_bin = None
        self.capture_thread = None

        # create array which tracks currently marked packets
        self.marked_packets = dict()
        self.seen = set()
        self.duplicates = set()

        # set open/save file and quit application function
        self.actionOpen_Multi_Files.triggered.connect(self.open_multiple_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionLoadCapture.triggered.connect(self.open_file)
        self.actionSaveCapture.triggered.connect(self.save_as_file)
        self.actionNextPacket.triggered.connect(self.next_packet)
        self.actionPreviousPacket.triggered.connect(self.previous_packet)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_As_2.triggered.connect(self.save_as_file)
        self.actionExit.triggered.connect(self.quit)

        # set the capture menu
        self.actionStart.triggered.connect(self.start_capture)
        self.actionStop.triggered.connect(self.stop_capture)
        self.actionPause.triggered.connect(self.pause_capture)

        # set the analysis menu
        self.actionGraph.triggered.connect(self.graph)
        self.actionAttack_Analysis.triggered.connect(self.attack_analysis)

        # set the help menu
        self.actionUse_Guide.triggered.connect(self.use_guide)

        # set display filter
        self.filterBox.setEditable(True)
        self.filterBox.pFilterModel = QSortFilterProxyModel(self)
        self.filterBox.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterBox.pFilterModel.setSourceModel(self.filterBox.model())

        self.filterBox.completer = QCompleter(self.filterBox.pFilterModel, self)

        self.filterBox.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.filterBox.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.filterBox.setCompleter(self.filterBox.completer)

        self.filterBox.lineEdit().textEdited.connect(self.filterBox.pFilterModel.setFilterFixedString)
        self.filterBox.completer.activated.connect(self.completer_operate)

        self.filterBot.clicked.connect(self.filter_capture)

        self.filter_list = ["", "ARP", "DNS", "ICMP", "IGMP", "IPv6", "UDP", "TCP"]
        self.filterBox.addItems(self.filter_list)

        # set capture list
        self.captureList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.captureList.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.captureList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.captureList.verticalHeader().setVisible(False)
        self.captureList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.captureList.cellClicked.connect(self.get_select_packet)
        self.captureList.cellClicked.connect(self.get_current_list_row)
        self.captureList.cellDoubleClicked.connect(self.handle_double_clicked_row)

        # set sub window
        self.subs = []

        # set graph window
        self.graph_window = None
        self.attack_analysis_window = None

        # start button pressed
        self.actionStartCapture.triggered.connect(self.start_capture)
        # pause button pressed
        self.actionPauseCapture.triggered.connect(self.pause_capture)
        self.actionPauseCapture.setEnabled(False)
        # stop button pressed
        self.actionStopCaputure.triggered.connect(self.stop_capture)
        self.actionStopCaputure.setEnabled(False)

        # set status bar
        self.statusBar.showMessage('Ready for Capturing')

        # set edit tool
        self.actionCopy.triggered.connect(self.copy)
        self.actionFindNextPacket.triggered.connect(self.next_packet)
        self.actionFindPreviousPacket.triggered.connect(self.previous_packet)
        self.actionMarkPacket.triggered.connect(self.mark_packet)
        self.actionMarkAllDisplayed.triggered.connect(self.mark_all_displayed)
        self.actionUnmarkAllDisplayed.triggered.connect(self.unmark_all_displayed)
        self.actionIgnorePacket.triggered.connect(self.ignore_packet)
        self.actionIgnoreAllDisplayed.triggered.connect(self.ignore_all_displayed)
        self.actionUnignoreAllDisplayed.triggered.connect(self.unignore_all_displayed)

    # Helper function to get the current row of the capture list
    def get_current_list_row(self):
        row = self.captureList.currentRow()
        return row

    # Helper function to get the selected packet and its details from the capture list based on the row number
    def get_select_packet(self, row):
        item = self.captureList.item(row, 0)
        # if the filtered packets are empty, select the sniffed packets
        if not self.GUI_actions.sniffer.filtered_packets:
            selected_packet = self.GUI_actions.sniffer.sniffed_packets[int(item.text()) - 1]
        # otherwise show the filtered packets
        else: 
            selected_packet = self.GUI_actions.sniffer.filtered_packets[int(item.text()) - 1]
        details = str.splitlines(selected_packet.show(dump=True))
        return selected_packet, details

    # select the next packet
    def next_packet(self):
        if self.captureList.rowCount() == 0:
            return
        else:
            next_row = (self.get_current_list_row() + 1) % self.captureList.rowCount()
            self.captureList.setCurrentCell(next_row, 0)

    # select the previous packet
    def previous_packet(self):
        if self.captureList.rowCount() == 0:
            return
        else:
            prev_row = (self.get_current_list_row() - 1) % self.captureList.rowCount()
            self.captureList.setCurrentCell(prev_row, 0)

    # Puts the data of the packet into a tree structure to make it easier to read
    def display_packet_detail(self, detail):
        root_amount = 0
        root_arr = []
        root_name = []
        root_index_arr = []
        for i in range(len(detail)):
            # Identify the root element of the packet
            if detail[i].__contains__('[ '):
                root_amount += 1
                temp = detail[i].strip('|###[ ')
                temp2 = temp.strip(' ]###')
                root_name.append(temp2)
                root_index_arr.append(i)
            else:
                root_index_arr.append(' ')

        

        temp_index = 0
        for i in range(len(detail)):
            if i == 0:
                continue
            if i == root_index_arr[i]:
                temp_index += 1
                if temp_index >= root_amount:
                    temp_index = root_amount - 1
                continue
            QTreeWidgetItem(root_arr[temp_index]).setText(0, detail[i])

    # if a row is double-clicked, display the packets detail in new window (subWindow)
    def handle_double_clicked_row(self, row):
        length = len(self.subs)
        # Add the new subWindow to the subs list, which is used to keep track of all the subWindows
        self.subs.append(subWindow.SubWindow())
        selected_packet, details = self.get_select_packet(row)
        # self.subs[length].parse_packet(selected_packet)
        self.subs[length].setWindowTitle("Packet #" + str(row + 1) + "  " + str(selected_packet.sprintf(
            "%Ether.type%"
        )))
        # Display the packet detail in the newly created subWindow
        self.subs[length].display_packet_data(selected_packet)
        self.subs[length].display_packet_detail(details)
        self.subs[length].show()
        
    # open a single pcap file
    def open_file(self):
        self.actionStopCaputure.setEnabled(True)
        self.stopped_capture = False
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", 'pcap (*.pcap);;All files (*)')
        if file_name:
            self.GUI_actions.read_pcap(str(file_name), mainWindow)
        else:
            self.stop_capture()

    # opens pcap file(s) and displays its content
    def open_multiple_file(self):
        self.actionStopCaputure.setEnabled(True)
        self.stopped_capture = False
        # gets the filename of the selected files
        file_names, _ = QFileDialog.getOpenFileNames(self, "Open files", "", 'pcap (*.pcap);;All files (*)')
        length = len(file_names)
        temp = 0
        while temp < length:
            if file_names[temp] != '':
                self.GUI_actions.read_pcap(str(file_names[temp]), mainWindow)
            temp += 1

    # saves a pcap file of the captured packets
    def save_file(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save file', "", 'pcap (*.pcap);;All files (*)')
        if file_name[0] == '':
            return
        self.GUI_actions.write_pcap(str(os.path.basename(file_name[0])))

    # saves a pcap file of the captured packets as a new file
    def save_as_file(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save As', '', 'pcap (*.pcap);;All files (*)')
        if file_name[0] == '':
            return
        self.GUI_actions.write_pcap(str(file_name[0]))

    # closes the GUI window
    def quit(self):
        self.close()

    # pauses the packet capturing, does not remove packets, and doesn't reset packet counter
    def pause_capture(self):
        # disables/enables the buttons
        self.actionStartCapture.setEnabled(True)
        self.actionPauseCapture.setEnabled(False)
        self.actionStopCaputure.setEnabled(True)
        # stops the sniffer
        self.GUI_actions.start_sniffer(False, mainWindow)

    # stops the packet capturing
    def stop_capture(self):
        self.marked_packets.clear()
        self.actionStartCapture.setEnabled(True)
        self.actionPauseCapture.setEnabled(False)
        self.actionStopCaputure.setEnabled(False)

        # variable used to remove captured packets from display
        self.stopped_capture = True
        self.captureList.setRowCount(0)
        self.GUI_actions.start_sniffer(False, mainWindow)
        self.packet_number = 1
        # resets captured packets
        self.GUI_actions.sniffer.reset()

    # method to start sniffer, ran as thread so packets are displayed dynamically
    def start_capture_thread(self):
        self.stopped_capture = False
        self.GUI_actions.sniffer.set_sniff_amount(self.lineEdit.text())
        self.GUI_actions.sniffer.set_filter(self.filterBox.currentText())
        # calls method in GUI_actions to start sniffer, passes window object through
        try:
            self.GUI_actions.start_sniffer(True, mainWindow)
        except PermissionError:
            self.permission_allowed.emit()

    # handles error raised by sniffer if user does not have capture permissions     
    def handle_permision_error(self):
        sys.stderr.write("PermissionError: You do not have permission to capture...\n")
        sys.stderr.flush()
        self.stop_capture()
        self.open_alert("Permission Error", "You are not allowed to capture packets")
    
    # initialises and starts packet capture thread
    def start_capture(self):
        self.actionStartCapture.setEnabled(False)
        self.actionPauseCapture.setEnabled(True)
        self.actionStopCaputure.setEnabled(True)
        # creates a thread to run simultaneously so the user can still interact with GUI
        self.capture_thread = threading.Thread(target=self.start_capture_thread)
        # starts running the thread
        self.capture_thread.start()
        
    # open the graph subwindow
    def graph(self):
        data = self.GUI_actions.get_sniffed_packets()
        plot = plotting.Plotting(data)
        plot.run_all()

    # open the attack analysis subwindow
    def attack_analysis(self):
        data = self.GUI_actions.get_sniffed_packets()
        attack_analysis = attack_analysis_action.AttackAnalysis(data, self.flaggedIPs)
        attack_analysis.run_all_detect()

    def use_guide(self):
        # project_root = os.path.abspath(os.path.dirname(__file__))
        # file_path = f"file://{project_root}/help_resource/index.html"
        # webbrowser.open(file_path)
        webbrowser.open_new_tab('https://ubiquitous-sniffle-y217w7w.pages.github.io/#/')

    # filters captured packets
    def filter_capture(self):
        # gets new list of filtered packets
        filtered_packets = self.GUI_actions.filter_packets(self.filterBox.currentText())
        # removes packets from display
        self.captureList.setRowCount(0)
        self.packet_number = 1
        # displays each packet
        for packet in filtered_packets:
            self.display_packet(packet)
        self.reapply_markers()
        
    # in order to use PyQts build in sorting function for tables with integers,
    # need to store integers using this custom item class which allows integer comparison
    class TableItemInt(QTableWidgetItem):
        # less than initializer that allows two items to be compared.
        def __lt__(self, other):
            return int(self.text()) < int(other.text())

    # called whenever a packet is captured by the sniffer, displays this packet in a table
    def display_packet(self, packet):
        # gets current amount of rows
        row_number = self.captureList.rowCount()
        self.captureList.insertRow(row_number)
        # first column for packet number
        packet_number_item = self.TableItemInt(str(self.packet_number))
        self.captureList.setItem(row_number, 0, packet_number_item)
        # 2nd column for timestamp
        self.captureList.setItem(row_number, 1, QTableWidgetItem(
            str(datetime.fromtimestamp(int(packet.time)))))
        # depending on the layers of the packet attributes need to be handled differently
        if packet.haslayer(IP):
            # 3rd column = source address
            self.captureList.setItem(row_number, 2, QTableWidgetItem(packet.getlayer(IP).src))

            # 4th column = destination address
            self.captureList.setItem(row_number, 3, QTableWidgetItem(packet.getlayer(IP).dst))

            # 5th column = protocol obtained from calling function to get protocol name from protocol number
            self.captureList.setItem(row_number, 4,
                                     QTableWidgetItem(
                                         str(self.GUI_actions.get_protocol(packet.getlayer(IP).proto, packet))))

            # 6th column = length of packet
            packet_len_item = self.TableItemInt(str(len(packet)))
            self.captureList.setItem(row_number, 5, packet_len_item)

            # updates capture list for each packet
            self.captureList.update()
            # allows scroll bar to follow most recent captured packet
            self.captureList.verticalScrollBar().setSliderPosition(row_number)
            
            if self.GUI_actions.get_protocol(packet.getlayer(IP).proto, packet) == "TCP":
                self.set_background(row_number, 0, 51, 102)
            elif self.GUI_actions.get_protocol(packet.getlayer(IP).proto, packet) == "UDP" or self.GUI_actions.get_protocol(packet.getlayer(IP).proto, packet) == "UDP/DNS":
                self.set_background(row_number, 0, 102, 51)
            elif self.GUI_actions.get_protocol(packet.getlayer(IP).proto, packet) == "IGMP":
                self.set_background(row_number, 102, 0, 102)
            elif self.GUI_actions.get_protocol(packet.getlayer(IP).proto, packet) == "ICMP":
                self.set_background(row_number, 0, 102, 102)


        # Handles the case where the packet has an ARP layer
        elif packet.haslayer(ARP):
            # The capture list is updated with the source and destination IP addresses
            self.captureList.setItem(row_number, 2, QTableWidgetItem(packet.getlayer(ARP).psrc))

            self.captureList.setItem(row_number, 3, QTableWidgetItem(packet.getlayer(ARP).pdst))

            self.captureList.setItem(row_number, 4,
                                     QTableWidgetItem("ARP"))

            # The capture list is updated with the length of the packet
            # TableItemInt is used to allow the table to sort the length of the packet
            packet_len_item = self.TableItemInt(str(len(packet)))
            self.captureList.setItem(row_number, 5, packet_len_item)
            
            # The capture list is updated
            self.captureList.update()
            self.captureList.verticalScrollBar().setSliderPosition(row_number)
            self.set_background(row_number, 102, 0, 0)

        # Handles the case where the packet has an IPv6 layer
        elif packet.haslayer(IPv6):
            
            self.captureList.setItem(row_number, 2, QTableWidgetItem(packet.getlayer(IPv6).src))

            self.captureList.setItem(row_number, 3, QTableWidgetItem(packet.getlayer(IPv6).dst))

            # The capture list is updated with the protocol for the packet
            self.captureList.setItem(row_number, 4,
                                     QTableWidgetItem(
                                         str(self.GUI_actions.get_protocol(packet.getlayer(IPv6).nh, packet))))

            # The capture list is updated as above
            packet_len_item = self.TableItemInt(str(len(packet)))
            self.captureList.setItem(row_number, 5, packet_len_item)

            self.captureList.update()
            self.captureList.verticalScrollBar().setSliderPosition(row_number)
            self.set_background(row_number, 102, 102, 0)

        # if the packet capture has been stopped
        if self.stopped_capture:
            # empties the table
            self.captureList.setRowCount(0)
            # resets packet counter to 1
            self.packet_number = 0
            self.captureList.update()
            self.captureList.verticalScrollBar().setSliderPosition(row_number)

        # updates the status bar to show the amount of packets captured
        packet_total = "Packets: " + str(self.packet_number)
        self.statusBar.showMessage(packet_total)

        # increments packet number for each captured packet
        self.packet_number += 1
        self.find_duplicates(packet)

    # set background color for a row depending on the packet's protocol
    def set_background(self, row_number, red, green, blue):
        self.captureList.item(row_number, 0).setBackground(QColor(red, green, blue))
        self.captureList.item(row_number, 1).setBackground(QColor(red, green, blue))
        self.captureList.item(row_number, 2).setBackground(QColor(red, green, blue))
        self.captureList.item(row_number, 3).setBackground(QColor(red, green, blue))
        self.captureList.item(row_number, 4).setBackground(QColor(red, green, blue))
        self.captureList.item(row_number, 5).setBackground(QColor(red, green, blue))

    # method to display the byte version of the packet
    # currently displays data but would like, so it shows in the detail section the selected bytes
    def display_packet_data(self, packet):
        # clears any previous data
        self.data.clear()
        packet_data = bytes(packet)
        # converts the packet data into a hex string
        hex_data = hex_packet_data(packet_data)
        datas = hex_data.split(' --- ')
        length = len(datas)
        label_num = 0
        hex_num = 1
        text_num = 2

        # extracts the labels (every 3rd element starting at 0)
        labels = []
        while label_num <= length - 3:
            labels.append(datas[label_num])
            label_num += 3

        # extracts the hex data (every 3rd element starting at 1)
        hex_datas = []
        while hex_num <= length - 2:
            hex_datas.append(datas[hex_num])
            hex_num += 3

        # extracts the text data (every 3rd element starting at 2)
        text_datas = []
        while text_num <= length - 1:
            text_datas.append(datas[text_num])
            text_num += 3

        # sets the number of rows in the table
        row_number = length / 3
        self.data.setRowCount(int(row_number))
        self.data.setColumnCount(32)

        try:
            self.data.setVerticalHeaderLabels(labels)
            current_row = 0
            while current_row < int(row_number):
                # splits the hex data into a list of bytes
                hex_data_current = hex_datas[current_row]
                hex_data_current_split = hex_data_current.split(' ')
                hex_data_helper = 0
                # loops through the first 16 bytes of the packet
                while hex_data_helper < 16:
                    if hex_data_helper >= len(hex_data_current_split):
                        break
                    # create a table item for each byte
                    self.data.setItem(int(current_row), hex_data_helper,
                                      QTableWidgetItem(str(hex_data_current_split[hex_data_helper])))
                    hex_data_helper += 1
                # splits the text data into a list of bytes similar to above
                text_data_current = text_datas[current_row]
                text_data_current_split = text_data_current.split(' ')
                text_data_helper1 = 16
                text_data_helper2 = 0
                # loops through the last 16 bytes of the packet
                while text_data_helper1 < 32:
                    if text_data_helper2 >= len(text_data_current_split):
                        break
                    # create a table item for each byte
                    self.data.setItem(int(current_row), text_data_helper1,
                                      QTableWidgetItem(str(text_data_current_split[text_data_helper2])))
                    text_data_helper1 += 1
                    text_data_helper2 += 1
                # move on to the next row of data
                current_row += 1
        # displays "NO DATA" if there is no data
        except:
            self.data.setItem(0, 0, QTableWidgetItem("NO DATA"))

        self.actionTurnHex.setCheckable(True)
        self.actionTurnBin.setCheckable(True)
        self.actionTurnHex.setChecked(True)
        self.actionTurnBin.setChecked(False)

        self.show_in_hex = True
        self.show_in_bin = False

    # create a menu for the data box when the user right clicks
    def create_rightMenu(self):

        # add a checkbox to the menu
        self.actionTurnBin.setCheckable(True)
        self.data_box_menu.addAction(self.actionTurnBin)

        self.actionTurnHex.setCheckable(True)
        self.data_box_menu.addAction(self.actionTurnHex)
        
        # display the menu at the current cursor position
        self.data_box_menu.popup(QCursor.pos())

    # display the packet data in binary
    def show_data_bin(self, packet):
        # clear any previous data
        self.data.clear()
        # convert the packet data into a list of bytes which are stored in datas
        packet_data = bytes(packet)
        hex_data = hex_packet_data(packet_data)
        datas = hex_data.split(' --- ')
        length = len(datas)
        # sets some variables to be used in the while loops below
        label_num = 0
        hex_num = 1
        text_num = 2
        print(datas)

        # extract the labels (every 3rd element starting at 0)
        labels = []
        while label_num <= length - 3:
            labels.append(datas[label_num])
            label_num += 3

        # extract the hex data (every 3rd element starting at 1)
        hex_datas = []
        while hex_num <= length - 2:
            hex_datas.append(datas[hex_num])
            hex_num += 3

        # extract the text data (every 3rd element starting at 2)
        text_datas = []
        while text_num <= length - 1:
            text_datas.append(datas[text_num])
            text_num += 3

        # set the number of rows in the table
        row_number = length / 3
        self.data.setRowCount(int(row_number))
        self.data.setColumnCount(32)

        try:
            # set the labels for the table
            self.data.setVerticalHeaderLabels(labels)
            current_row = 0
            # loops through each row of the table
            while current_row < int(row_number):
                hex_data_current = hex_datas[current_row]
                hex_data_current_split = hex_data_current.split(' ')
                
                # convert hex data to binary
                index = 0
                hex_data_fin = []
                while index < len(hex_data_current_split):
                    if hex_data_current_split[index] != '':
                        hex_data_fin.append(hex_data_current_split[index])
                    index += 1


                bin_data_current_split = []
                for x in hex_data_fin:
                    bin_data_current_split.append(bin(int(str(x), 16))[2:].zfill(2 * 4))

                bin_data_helper = 0
                # handles the binary representation of the packet data
                while bin_data_helper < 16:
                    if bin_data_helper >= len(bin_data_current_split):
                        break
                    # sets the item at the current row and column to be the binary data
                    self.data.setItem(int(current_row), bin_data_helper,
                                      QTableWidgetItem(bin_data_current_split[bin_data_helper]))
                    bin_data_helper += 1
                text_data_current = text_datas[current_row]
                text_data_current_split = text_data_current.split(' ')
                text_data_helper1 = 16
                text_data_helper2 = 0
                # handles the text representation of the packet data
                while text_data_helper1 < 32:
                    if text_data_helper2 >= len(text_data_current_split):
                        break
                    self.data.setItem(int(current_row), text_data_helper1,
                                      QTableWidgetItem(str(text_data_current_split[text_data_helper2])))
                    text_data_helper1 += 1
                    text_data_helper2 += 1
                # move on to the next row of data
                current_row += 1
        except:
            self.data.setItem(0, 0, QTableWidgetItem("NO DATA"))

        self.actionTurnBin.setCheckable(True)
        self.actionTurnHex.setCheckable(True)
        self.actionTurnBin.setChecked(True)
        self.actionTurnHex.setChecked(False)

        self.show_in_hex = False
        self.show_in_bin = True

    # display the packet data in hexadecimal
    def operate_turn_hex(self):
        row = self.get_current_list_row()
        # gets the selected packet and its details
        selected_packet, details = self.get_select_packet(row)
        if self.show_in_bin:
            self.display_packet_data(selected_packet)

        self.actionTurnHex.setCheckable(True)
        self.actionTurnBin.setCheckable(True)
        self.actionTurnHex.setChecked(True)
        self.actionTurnBin.setChecked(False)
        # sets variables to show that the data is now in hexadecimal
        self.show_in_hex = True
        self.show_in_bin = False

    # display the packet data in binary in the same way as above
    def operate_turn_bin(self):
        row = self.get_current_list_row()
        selected_packet, details = self.get_select_packet(row)
        if self.show_in_hex:
            self.show_data_bin(selected_packet)

        self.actionTurnBin.setCheckable(True)
        self.actionTurnHex.setCheckable(True)
        self.actionTurnBin.setChecked(True)
        self.actionTurnHex.setChecked(False)
        self.show_in_hex = False
        self.show_in_bin = True

    # autocomplete the input in the filter box
    def completer_operate(self, text):
        # if the text is not an empty string
        if text:
            # find the index of the text in the filter list
            index = self.filterBox.findText(text)
            self.filterBox.setCurrentIndex(index)

    # update the filter and completer model when model has changed
    def set_model(self, model):
        super(QComboBox, self.filterBox).setModel(model)
        # sets the source model of the filter model using the given model
        self.filterBox.pFilterModel.setSourceModel(model)
        self.filterBox.completr.setModel(self.filterBox.pFilterModel)

    # update the filter and completer model when model column has changed
    def set_model_column(self, column):
        self.filterBox.completer.setCompletionColumn(column)
        self.filterBox.pFilterModel.setFilterKeyColumn(column)
        super(QComboBox, self.filterBox).setModelColumn(column)

    # copies selected packet details to clipboard
    def copy(self):
        if self.captureList.rowCount() == 0:
            return
        row = self.get_current_list_row()
        _, details = self.get_select_packet(row)
        clipboard = QApplication.clipboard()
        clipboard.clear()
        details_str = '\n'.join(details)
        clipboard.setText(details_str)

    # gets all rows that have been selected
    def get_selected_rows(self):
        selected_indexes = self.captureList.selectionModel().selectedRows()
        selected_rows = [index.row() for index in selected_indexes]
        return selected_rows

    # data class to keep track of a marked packet, its hash, and its previous colour prior to marking
    @dataclass
    class MarkedPacket:
        hash: int
        r: int
        g: int
        b: int
        ignored: bool
        marked: bool
    
    # finds all duplicates, used only in marking
    def find_duplicates(self, packet):
        details = str.splitlines(packet.show(dump=True))
        hashed = hashlib.sha256((str(packet.time) + ''.join(details)).encode('utf-8')).hexdigest()
        if hashed not in self.seen:
            self.seen.add(hashed)
        else:
            self.duplicates.add(hashed)
        
    # given a row, hash a packet using its encoded details
    def hash_packet(self, row):
        packet, details = self.get_select_packet(row)
        # append the time to the packet details, thus ensuring packets with the same
        # details aren't considered duplicates (A duplicate should be seen as two packets
        # that are virtually indistinguishable, not two packets with the same "details")
        tag = (str(packet.time) + ''.join(details)).encode('utf-8')
        return hashlib.sha256(tag).hexdigest()
    
    # on every filter, reapply markings to packets
    def reapply_markers(self):
        for row in range(self.captureList.rowCount()):
            hashed_packet = self.hash_packet(row)
            if self.hash_packet(row) in self.marked_packets:
                if self.marked_packets[hashed_packet].ignored:
                    self.set_background(row, 255, 255, 255)
                else:
                    self.set_background(row, 0, 0, 0)

    # returns row with a packet from a specific hash, used for duplicate packets
    def get_rows_from_hash(self, hash):
        rows = []
        for row in range(self.captureList.rowCount()):
            dup_hash = self.hash_packet(row)
            if dup_hash in self.duplicates and dup_hash == hash:
                rows.append(row)
        return rows

    # create a message box warning user of a marking conflict
    def open_alert(self, title, warning):
        msgBox = message.MarkWaring(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(warning)
        msgBox.exec_()

    # logic for marking a packet, as either a packet of interest or ignoring it
    def marker(self, row, ignore, mark):
        cell = self.captureList.item(row, 0)
        hashed_packet = self.hash_packet(row)
        # check if packet is already marked
        if hashed_packet in self.marked_packets:
            # unmark by restoring to original color
            marked_packet = self.marked_packets[hashed_packet]
            # if we try to mark and ignored packet, or ignore a marked packet, we launch a message box warning us
            if (ignore and marked_packet.marked) or (marked_packet.ignored and mark):
                self.open_alert("Marking Warning", "You are trying to mark an ignored packet, or ignore a marked packet")
                return 1
            # if this packet is a duplicate, we unmark all duplicates
            if marked_packet.hash in self.duplicates:
                duplicate_rows = self.get_rows_from_hash(marked_packet.hash)
                for dup in duplicate_rows:
                    self.set_background(dup, marked_packet.r, marked_packet.g, marked_packet.b)
                    if ignore:
                        packet, _ = self.get_select_packet(dup)
                        self.GUI_actions.sniffer.ignored_packets.append(packet)
            else:
                self.set_background(row, marked_packet.r, marked_packet.g, marked_packet.b)
                if ignore:
                    packet, _ = self.get_select_packet(row)
                    self.GUI_actions.sniffer.ignored_packets.append(packet)
            del self.marked_packets[marked_packet.hash]
        # mark packet if it hasn't been marked
        else:
            previous_color = cell.background().color()
            red, green, blue = (previous_color.red(), previous_color.green(), previous_color.blue())
            marked_packet = self.MarkedPacket(hashed_packet, red, green, blue, False, True)
            if ignore:
                marked_packet.ignored = True
                marked_packet.marked = False
            # if this packet is a duplicate, we will mark all duplicates
            if hashed_packet in self.duplicates:
                duplicate_rows = self.get_rows_from_hash(hashed_packet)
                if ignore:
                    marked_packet.ignored = True
                    marked_packet.marked = False
                for dup in duplicate_rows:
                    if ignore:
                        self.set_background(dup, 255, 255, 255)
                        packet, _ = self.get_select_packet(row)
                        self.GUI_actions.sniffer.ignored_packets.append(packet)
                    else:
                        self.set_background(dup, 0, 0, 0)
            else:
                if ignore:
                    packet, _ = self.get_select_packet(row)
                    self.GUI_actions.sniffer.ignored_packets.append(packet)
                    self.set_background(row, 255, 255, 255)
                else:
                    self.set_background(row, 0, 0, 0)
            self.marked_packets[marked_packet.hash] = marked_packet
                
    # mark or unmark packet(s)
    def mark_packet(self):
        selected_rows = self.get_selected_rows()
        local_duplicates = set()
        for row in selected_rows:
            hash = self.hash_packet(row)
            # if there are duplicates in your selected rows, then mark will only run once, which will mark all duplicates
            if hash in local_duplicates:
                continue
            if hash in self.duplicates:
                local_duplicates.add(hash)
            if self.marker(row, False, True) == 1:
                return

    # mark all visible packets
    def mark_all_displayed(self):
        local_duplicates = set()
        for row in range(self.captureList.rowCount()):
            hash = self.hash_packet(row)
            if hash not in self.marked_packets:
                # if there are duplicates in your selected rows, the mark will only run once, which will mark all duplicates
                if hash in local_duplicates:
                    continue
                if hash in self.duplicates:
                    local_duplicates.add(hash)
                if self.marker(row, False, True) == 1:
                    return
        
    # unmark all visible packets
    def unmark_all_displayed(self):
        local_duplicates = set()
        for row in range(self.captureList.rowCount()):
            hash = self.hash_packet(row)
            if hash in self.marked_packets:
                # if there are duplicates in your selected rows, the mark will only run once, which will mark all duplicates
                if hash in local_duplicates:
                    continue
                if hash in self.duplicates:
                    local_duplicates.add(hash)
                if self.marked_packets[hash].marked:
                    if self.marker(row, False, True) == 1:
                        return

    # mark a packet or packets as ignored, or unmark it as such
    def ignore_packet(self):
        selected_rows = self.get_selected_rows()
        local_duplicates = set()
        for row in selected_rows:
            hash = self.hash_packet(row)
            if hash in local_duplicates:
                continue
            if hash in self.duplicates:
                local_duplicates.add(hash)
            if self.marker(row, True, False) == 1:
                return

    # ignores all visible packets
    def ignore_all_displayed(self):
        local_duplicates = set()
        for row in range(self.captureList.rowCount()):
            hash = self.hash_packet(row)
            if hash not in self.marked_packets:
                if hash in local_duplicates:
                    continue
                if hash in self.duplicates:
                    local_duplicates.add(hash)
                if self.marker(row, True, False) == 1:
                    return

    # removes all markings that say a packet is ignored for visible packets
    def unignore_all_displayed(self):
        local_duplicates = set()
        for row in range(self.captureList.rowCount()):
            hash = self.hash_packet(row)
            if hash in self.marked_packets:
                if hash in local_duplicates:
                    continue
                if hash in self.duplicates:
                    local_duplicates.add(hash)
                if self.marked_packets[hash].ignored:
                    if self.marker(row, True, False) == 1:
                        return

    # use <ENTER> in filter box of the GUI to select filter
    def enter_keypress(self, key): # key refers to the key that was pressed
        # if the key pressed is the enter key
        if key.key() == Qt.Key_Enter & key.key() == Qt.Key_Return:
            # get the text and index of the text from the filter box
            text = self.filterBox.currentText()
            index = self.filterBox.findText(text, Qt.MatchExactly | Qt.MatchCaseSensitive)
            self.filterBox.setCurrentIndex(index)
            # hide the dropdown list
            self.filterBox.hidePopup()
        super(QComboBox, self.filterBox).enter_keypress(key)

# ran first and intialises PyQt window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.permission_allowed.connect(mainWindow.handle_permision_error)
    app.setStyle('Fusion')
    mainWindow.show()
    sys.exit(app.exec_())

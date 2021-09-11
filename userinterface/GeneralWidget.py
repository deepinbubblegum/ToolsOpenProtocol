import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call
from qtwidgets import Toggle, AnimatedToggle
from model.SQLControler import sqlControler

class ForSizeOnlyDelegate(QItemDelegate):
    def sizeHint(self, option, index):
        return QSize(38, 38)

class GeneralWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneralWidget, self).__init__(parent)
        
        self._sqlControler = sqlControler('./database/openprotocol.db')
        res_tools = self._sqlControler.db_QuerySQL(
            'SELECT * FROM Tools'
        )

        VLayout = QVBoxLayout(self)
        HLayout1 = QHBoxLayout()
        HLayout2 = QHBoxLayout()
        HLayout3 = QHBoxLayout()
        HLayout4 = QHBoxLayout()
        VLayout.addLayout(HLayout1)
        VLayout.addLayout(HLayout2)
        VLayout.addLayout(HLayout4)
        VLayout.addLayout(HLayout3)
        VLayout.addStretch()

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        regex = QRegExp(
            "^" + ipRange
            + "\\." + ipRange
            + "\\." + ipRange
            + "\\." + ipRange
            + "$"
        )
        validator = QRegExpValidator(regex)

        label_IPAddress = QLabel("IP Address :")
        self.editText_IPAddress = QLineEdit(self)
        self.editText_IPAddress.setPlaceholderText("255.255.255.255")
        self.editText_IPAddress.setValidator(validator)
        
        self.ip_address_Button = QPushButton("Save Change")
        self.ip_address_Button.clicked.connect(self.on_click_Ip_save)
        
        HLayout1.addWidget(label_IPAddress)
        HLayout1.addWidget(self.editText_IPAddress)
        HLayout1.addWidget(self.ip_address_Button)
        

        label_Tools = QLabel("Tools :")
        self.combo_Tools = QComboBox(self)
        for row in res_tools:
            self.combo_Tools.addItem(row[1])

        self.combo_Tools.currentIndexChanged.connect(
            self.on_combo_Tools_changed)
        self.combo_Tools.setCurrentIndex(0)

        toggle_ByPass = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )
        toggle_ByPass.adjustSize()
        label_ByPass = QLabel("By Pass :")

        label_Link_ID = QLabel("Link ID :")
        self.combo_Link_ID = QComboBox(self)
        self.combo_Link_ID.currentIndexChanged.connect(
            self.on_combo_Link_changed)

        HLayout2.addWidget(label_Tools)
        HLayout2.addWidget(self.combo_Tools, 3)

        HLayout2.addWidget(label_ByPass)
        HLayout2.addWidget(toggle_ByPass)

        HLayout2.addWidget(label_Link_ID)
        HLayout2.addWidget(self.combo_Link_ID, 1)

        delegate = ForSizeOnlyDelegate()
        self.table = QTableWidget(self)
        self.table.setItemDelegate(delegate)

        # self.table.setAcceptDrops(True)
        # self.table.setDragEnabled(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.resizeColumnsToContents()

        HLayout3.addWidget(self.table)

        label_addTRAY = QLabel("Tray ID :")
        self.combo_addTRAY = QComboBox(self)

        label_addSocket = QLabel("Socket ID :")
        self.combo_addSocket = QComboBox(self)

        addButton = QPushButton("Add Step")
        addButton.clicked.connect(self.on_click_addStep)

        HLayout4.addWidget(label_addTRAY)
        HLayout4.addWidget(self.combo_addTRAY, 1)

        HLayout4.addWidget(label_addSocket)
        HLayout4.addWidget(self.combo_addSocket, 1)

        HLayout4.addWidget(addButton, 2)
        
        self.Select_Link_ID_Value = 1
        self.Select_Tools_Value = 1
        self.res_step = None

        # init sql
        self.Link_QuerySQL()
        self.GetDataSocket()
        self.GetDataTRAY()
        
        self.getIpAddress()
        
    def on_click_Ip_save(self):
        msgBox = QMessageBox()
        msgBox.setWindowFlags(
           Qt.Window |
           Qt.CustomizeWindowHint |
           Qt.WindowTitleHint |
           Qt.WindowCloseButtonHint |
           Qt.WindowStaysOnTopHint
        )
        reply = msgBox.question(
            self, 
            'Save IP Address', 
            'Are you sure you want to save change ip adress?', 
            QMessageBox.Yes | 
            QMessageBox.No, 
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            ipAddress = str(self.editText_IPAddress.text())
            self._sqlControler.db_Update_ip(ipAddress)
            self.getIpAddress()
            print('Save Change Ip Address.')
        else:
            pass
        
    def getIpAddress(self):
        res_step = self._sqlControler.db_QuerySQL(
            'SELECT IP_Address FROM IP'
        )
        self.editText_IPAddress.setText(res_step[0][0])

    def GetDataSocket(self):
        self.combo_addSocket.clear()
        res_socket = self._sqlControler.db_QuerySQL(
            'SELECT * FROM Socket'
        )
        for row in res_socket:
            self.combo_addSocket.addItem(str(row[1]))

    def GetDataTRAY(self):
        self.combo_addTRAY.clear()
        res_tray = self._sqlControler.db_QuerySQL(
            'SELECT * FROM TRAY'
        )
        for row in res_tray:
            self.combo_addTRAY.addItem(str(row[1]))

    def on_combo_Tools_changed(self, value):
        # print('Tools', value)
        self.Select_Tools_Value = value + 1
        self.getDataStep()

    def on_combo_Link_changed(self, value):
        self.Select_Link_ID_Value = value + 1
        # print('Link :',value)
        self.getDataStep()

    def Link_QuerySQL(self):
        self.combo_Link_ID.clear()
        res_link = self._sqlControler.db_QuerySQL(
            'SELECT * FROM Link'
        )
        for row in res_link:
            self.combo_Link_ID.addItem(str(row[1]))

    @pyqtSlot()
    def on_click_addStep(self):
        stepTRAY = str(self.combo_addTRAY.currentText())
        stepSocket = str(self.combo_addSocket.currentText())
        stepTools = str(int(self.combo_Tools.currentIndex()) + 1)
        stepLink_ID = str(self.combo_Link_ID.currentText())
        print(stepTRAY, stepSocket, stepTools, stepLink_ID)
        self._sqlControler.db_add_step(stepTRAY, stepSocket, stepTools, stepLink_ID)
        self.getDataStep()

    def getDataStep(self):
        if self.Select_Link_ID_Value is not None and self.Select_Tools_Value is not None:
            self.res_step = self._sqlControler.db_QuerySQL(
                'SELECT ID_STEP, ID_Link_step, ID_TRAY_ID, Socket_ID_Step FROM Step WHERE Step_Tools_ID = {} AND ID_Link_step = {} ORDER BY Step_number ASC'.format(self.Select_Tools_Value, self.Select_Link_ID_Value)
            )
            if len(self.res_step) > 0:
                self.table.setRowCount(len(self.res_step))
                self.table.setColumnCount(len(self.res_step[0])-1)
                for i, row in zip(range(len(self.res_step)), self.res_step):
                    for j, col in zip(range(len(row)), row):
                        if j >= 2:
                            self.table.setItem(i, j-2, QTableWidgetItem(str(col)))
                    self.btn_del = QPushButton('DELETE')
                    self.btn_del.clicked.connect(self.handleButtonClicked)
                    self.table.setCellWidget(i, len(self.res_step[0])-2, self.btn_del)
            else:
                while (self.table.rowCount() > 0):
                    self.table.removeRow(0)
        else:
            while (self.table.rowCount() > 0):
                self.table.removeRow(0)
                
        self.table.setHorizontalHeaderLabels(
            ["TRAY ID", "SOCKET ID", "COMMAND"])
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumSize(600, 280)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.resizeRowsToContents()
        self.table.scrollToBottom()

    def handleButtonClicked(self):
        button = qApp.focusWidget()
        # or button = self.sender()
        msgBox = QMessageBox()
        msgBox.setWindowFlags(
           Qt.Window |
           Qt.CustomizeWindowHint |
           Qt.WindowTitleHint |
           Qt.WindowCloseButtonHint |
           Qt.WindowStaysOnTopHint
        )
        reply = msgBox.question(
            self, 
            'Delete Step link', 
            'Are you sure you want to delete step ?', 
            QMessageBox.Yes | 
            QMessageBox.No, 
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            index = self.table.indexAt(button.pos())
            if index.isValid():
                ID_STEP = self.res_step[index.row()][0]
                ID_Link_step = self.res_step[index.row()][1]
                self._sqlControler.db_del_step(ID_STEP, ID_Link_step)
                print('Delete Step Success.')
                self.getDataStep()
        else:
            pass
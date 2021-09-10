import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call
from qtwidgets import Toggle, AnimatedToggle

import sqlite3


def QuerySQL(SQL):
    conn = sqlite3.connect('./database/openprotocol.db')
    cur = conn.cursor()
    cur.execute(SQL)
    res_data = cur.fetchall()
    conn.commit()
    conn.close()
    return res_data


class ForSizeOnlyDelegate(QItemDelegate):
    def sizeHint(self, option, index):
        # print("sizeHint", index.row(), index.column())
        return QSize(38, 38)


class GeneralWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneralWidget, self).__init__(parent)

        SQL_txt = 'SELECT * FROM Tools'
        res_tools = QuerySQL(SQL_txt)

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
        HLayout1.addWidget(label_IPAddress)
        HLayout1.addWidget(self.editText_IPAddress)

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

        label_addTRAY = QLabel("TRAY ID :")
        self.combo_addTRAY = QComboBox(self)

        label_addSocket = QLabel("SOCKET ID :")
        self.combo_addSocket = QComboBox(self)

        addButton = QPushButton("Add Step")
        addButton.clicked.connect(self.on_click_addStep)

        HLayout4.addWidget(label_addTRAY)
        HLayout4.addWidget(self.combo_addTRAY, 1)

        HLayout4.addWidget(label_addSocket)
        HLayout4.addWidget(self.combo_addSocket, 1)

        HLayout4.addWidget(addButton, 2)

        # init sql
        self.Link_QuerySQL()
        self.GetDataSocket(1)
        self.GetDataTRAY()
        
        self.getIpAddress()

    def GetDataSocket(self, value):
        self.combo_addSocket.clear()
        SQL_txt = 'SELECT * FROM Socket'
        res_socket = QuerySQL(SQL_txt)
        for row in res_socket:
            self.combo_addSocket.addItem(str(row[1]))

    def GetDataTRAY(self):
        self.combo_addTRAY.clear()
        SQL_txt = 'SELECT * FROM TRAY'
        res_tray = QuerySQL(SQL_txt)
        for row in res_tray:
            self.combo_addTRAY.addItem(str(row[1]))

    def on_combo_Tools_changed(self):
        self.Link_QuerySQL()

    def on_combo_Link_changed(self, value):
        value = value + 1
        self.getDataStep(5, 1)

    def Link_QuerySQL(self):
        self.combo_Link_ID.clear()
        SQL_txt = 'SELECT * FROM Link'
        res_link = QuerySQL(SQL_txt)
        for row in res_link:
            self.combo_Link_ID.addItem(str(row[1]))

    @pyqtSlot()
    def on_click_addStep(self):
        stepTRAY = str(self.combo_addTRAY.currentText())
        stepSocket = str(self.combo_addSocket.currentText())

    def getIpAddress(self):
        SQL_txt = "SELECT IP_Address FROM IP"
        res_step = QuerySQL(SQL_txt)
        # print(res_step[0][0])
        self.editText_IPAddress.setText(res_step[0][0])

    def getDataStep(self, Tools_ID, Id_Link):
        SQL_txt = "SELECT ID_TRAY_ID, Socket_ID_Step FROM Step WHERE Step_Tools_ID = {} AND ID_Link_step = {} ORDER BY Step_number ASC".format(Tools_ID, Id_Link)
        res_step = QuerySQL(SQL_txt)
        print(res_step)
        if len(res_step) > 0:
            self.table.setRowCount(len(res_step))
            self.table.setColumnCount(len(res_step[0])+1)
            for i, row in zip(range(len(res_step)), res_step):
                for j, col in zip(range(len(row)), row):
                    self.table.setItem(i, j, QTableWidgetItem(str(col)))
                self.btn_del = QPushButton('DELETE')
                self.btn_del.clicked.connect(self.handleButtonClicked)
                self.table.setCellWidget(i, len(res_step[0]), self.btn_del)
        else:
            while (self.table.rowCount() > 0):
                self.table.removeRow(0)

        self.table.setHorizontalHeaderLabels(
            ["TRAY ID", "SOCKET ID", "COMMAND"])
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumSize(600, 280)
        # self.table.setMaximumSize(600, 280)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.resizeRowsToContents()
        # self.table.adjustSize()

    def handleButtonClicked(self):
        button = qApp.focusWidget()
        # or button = self.sender()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            print(index.row(), index.column())

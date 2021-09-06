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

        label_IPAddress = QLabel("IP Address :")
        editText_IPAddress = QLineEdit(self)
        HLayout1.addWidget(label_IPAddress)
        HLayout1.addWidget(editText_IPAddress)

        label_Tools = QLabel("Tools :")
        self.combo_Tools = QComboBox(self)
        for row in res_tools:
            self.combo_Tools.addItem(row[1])
            
        self.combo_Tools.currentIndexChanged.connect(self.on_combo_Tools_changed)
        self.combo_Tools.setCurrentIndex(0)

        toggle_ByPass = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )
        toggle_ByPass.adjustSize()
        label_ByPass = QLabel("By Pass :")

        label_Link_ID = QLabel("Link ID :")
        self.combo_Link_ID = QComboBox(self)
        self.combo_Link_ID.currentIndexChanged.connect(self.on_combo_Link_changed)

        HLayout2.addWidget(label_Tools)
        HLayout2.addWidget(self.combo_Tools, 3)

        HLayout2.addWidget(label_ByPass)
        HLayout2.addWidget(toggle_ByPass)

        HLayout2.addWidget(label_Link_ID)
        HLayout2.addWidget(self.combo_Link_ID, 1)

        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setRowCount(5)
        # Set the table headers
        self.table.setHorizontalHeaderLabels(["STEP Number", "TRAY ID", "SOCKET ID", "COMMAND"])
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # Set the table values
        for i in range(1):
            for j in range(4) :
                self.table.setItem(i, j, QTableWidgetItem("STEP-" + str(i+1) + " , Col-" + str(j+1)))
        
        HLayout3.addWidget(self.table)

        self.onlyInt = QIntValidator()

        label_addStep = QLabel("Step :")
        self.editText_addStep = QLineEdit(self)
        self.editText_addStep.setValidator(self.onlyInt)

        label_addTRAY = QLabel("TRAY ID :")
        self.combo_addTRAY = QComboBox(self)

        label_addSocket = QLabel("SOCKET ID :")
        self.combo_addSocket = QComboBox(self)

        addButton = QPushButton("Add Step")
        addButton.clicked.connect(self.on_click_addStep)

        HLayout4.addWidget(label_addStep)
        HLayout4.addWidget(self.editText_addStep, 1)

        HLayout4.addWidget(label_addTRAY)
        HLayout4.addWidget(self.combo_addTRAY, 1)

        HLayout4.addWidget(label_addSocket)
        HLayout4.addWidget(self.combo_addSocket, 1)

        HLayout4.addWidget(addButton)
        
        # init sql
        self.Link_QuerySQL(0)
        self.GetDataSocket(1)
        self.GetDataTRAY()

    def GetDataSocket(self, value):
        self.combo_addSocket.clear()
        SQL_txt = 'SELECT * FROM Socket WHERE Socket_Tray_ID = ' + str(value)
        res_socket = QuerySQL(SQL_txt)
        for row in res_socket:
            self.combo_addSocket.addItem(str(row[1]))

    def GetDataTRAY(self):
        self.combo_addTRAY.clear()
        SQL_txt = 'SELECT * FROM TRAY'
        res_tray = QuerySQL(SQL_txt)
        for row in res_tray:
            self.combo_addTRAY.addItem(str(row[1]))

    def on_combo_Tools_changed(self, value):
        self.Link_QuerySQL(value)

    def on_combo_Link_changed(self, value):
        value = value + 1
        # print(value)
        self.getDataStep(value)

    def Link_QuerySQL(self, value):
        self.combo_Link_ID.clear()
        value = value + 1
        SQL_txt = 'SELECT * FROM Link WHERE ID_Tools_link = ' + str(value)
        res_link = QuerySQL(SQL_txt)
        for row in res_link:
            self.combo_Link_ID.addItem(str(row[1]))

    @pyqtSlot()
    def on_click_addStep(self):
        stepNumber = self.editText_addStep.text()
        stepTRAY = str(self.combo_addTRAY.currentText())
        stepSocket = str(self.combo_addSocket.currentText())
        self.editText_addStep.clear()

    def getDataStep(self, value):
        print('getDataStep')
        self.table.clear()
        SQL_txt = 'SELECT * FROM Step WHERE ID_Link_step = 1'
        res_step = QuerySQL(SQL_txt)
        table_i = 0
        table_j = 0
        self.table.setColumnCount(5)
        self.table.setRowCount(1)

        for i, rows in enumerate(res_step):
            for j, col in enumerate(rows):
                self.table.setItem(i, j, QTableWidgetItem("STEP-" + str(i+1) + " , Col-" + str(j+1)))
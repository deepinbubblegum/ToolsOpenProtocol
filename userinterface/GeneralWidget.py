import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call
from qtwidgets import Toggle, AnimatedToggle

class GeneralWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneralWidget, self).__init__(parent)
        VLayout = QVBoxLayout(self)
        HLayout1 = QHBoxLayout()
        HLayout2 = QHBoxLayout()
        HLayout3 = QHBoxLayout()
        VLayout.addLayout(HLayout1)
        VLayout.addLayout(HLayout2)
        VLayout.addLayout(HLayout3)
        VLayout.addStretch()

        label_IPAddress = QLabel("IP Address :")
        editText_IPAddress = QLineEdit(self)
        HLayout1.addWidget(label_IPAddress)
        HLayout1.addWidget(editText_IPAddress)

        label_Tools = QLabel("Tools :")
        combo_Tools = QComboBox(self)

        toggle_ByPass = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )
        toggle_ByPass.adjustSize()
        label_ByPass = QLabel("By Pass :")

        label_Link_ID = QLabel("Link ID :")
        combo_Link_ID = QComboBox(self)

        HLayout2.addWidget(label_Tools)
        HLayout2.addWidget(combo_Tools, 3)

        HLayout2.addWidget(label_ByPass)
        HLayout2.addWidget(toggle_ByPass)

        HLayout2.addWidget(label_Link_ID)
        HLayout2.addWidget(combo_Link_ID, 1)

        table = QTableWidget(self)
        table.setColumnCount(4)
        table.setRowCount(50)
        # Set the table headers
        table.setHorizontalHeaderLabels(["STEP ID", "TRAY ID", "SOCKET ID", "COMMAND"])
        table.setAlternatingRowColors(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # Set the table values
        for i in range(50):
            for j in range(4) :
                table.setItem(i, j, QTableWidgetItem("Row-" + str(i+1) + " , Col-" + str(j+1)))
        # Resize of the rows and columns based on the content
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        HLayout3.addWidget(table , 1)
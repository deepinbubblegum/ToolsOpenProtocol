import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call

class GeneralWidget(QWidget):
    def __init__(self, parent=None):
        super(GeneralWidget, self).__init__(parent)
        lay = QVBoxLayout(self)
        # Buttons
        button_start = QPushButton("start") #self.lang["btn_start"])
        button_stop = QPushButton("stop") #self.lang["btn_stop"])

        # Button Extra
        button_start.setToolTip("This is a tooltip for the button!")    # Message to show when mouse hover
        button_start.clicked.connect(self.on_click)

        button_stop.clicked.connect(self.on_click)

        lay.addWidget(button_start)
        lay.addWidget(button_stop)
        lay.addStretch()

    @pyqtSlot()
    def on_click(self):
        button = self.sender().text()
        if button == self.lang["btn_start"]:
            print("Dank")
        elif button == self.lang["btn_stop"]:
            print("Not dank")
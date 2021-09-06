import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call

class AdministratorWidget(QWidget):
    def __init__(self, parent=None):
        super(AdministratorWidget, self).__init__(parent)
        lay = QVBoxLayout(self)
        hlay = QHBoxLayout()
        lay.addLayout(hlay)
        lay.addStretch()

        label_exit = QLabel("Exit")
        exitButton = QPushButton("Exit")
        exitButton.clicked.connect(self.on_click_exit)

        hlay.addWidget(label_exit)
        hlay.addWidget(exitButton)

    @pyqtSlot()
    def on_click_exit(self):
    #     # os.system(cmd)
        QCoreApplication.instance().quit()
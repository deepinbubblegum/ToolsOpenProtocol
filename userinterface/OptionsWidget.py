import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call

class OptionsWidget(QWidget):
    def __init__(self, parent=None):
        super(OptionsWidget, self).__init__(parent)
        lay = QVBoxLayout(self)
        hlay = QHBoxLayout()
        lay.addLayout(hlay)
        lay.addStretch()

        label_language = QLabel("Language")
        combo_language = QComboBox(self)
        combo_language.addItem("item1") #self.lang["language_danish"])
        combo_language.addItem("item2") #self.lang["language_english"])
        hlay.addWidget(label_language)
        hlay.addWidget(combo_language)
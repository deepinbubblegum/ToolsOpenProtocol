import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call

class TabsWidget(QWidget):
    def __init__(self, parent):   
        super(TabsWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        # Run this after settings
        # self.lang = getLang(config.get("Main", "language"))
        # Initialize tabs
        tab_holder = QTabWidget()   # Create tab holder
        tab_1 = GeneralWidget()           # Tab one
        tab_2 = OptionsWidget()           # Tab two
        # Add tabs
        tab_holder.addTab(tab_1, "General") #self.lang["tab_1_title"]) # Add "tab1" to the tabs holder "tabs"
        tab_holder.addTab(tab_2, "Options") #self.lang["tab_2_title"]) # Add "tab2" to the tabs holder "tabs" 
        layout.addWidget(tab_holder)

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

    # def __init__(self, parent):
    #     super(QWidget, self).__init__(parent)
    #     self.layout = QVBoxLayout(self)

    #     # Initialize tab screen
    #     self.tabs = QTabWidget()
    #     self.tabController = QWidget()
    #     self.tabSettings = QWidget()
    #     self.tabRoot = QWidget()
    #     # self.tabs.resize(720,480)

    #     # Add tabs
    #     self.tabs.addTab(self.tabController,"Controller")
    #     self.tabs.addTab(self.tabSettings,"Settings")
    #     self.tabs.addTab(self.tabRoot, "#SU")

    #     self.tabController.layout = QVBoxLayout(self)
    #     self.tabSettings.layout = QVBoxLayout(self)
    #     self.tabRoot.layout = QVBoxLayout(self)
        
    #     # TabComponents init
    #     self.ControllerTabComponents()
    #     self.RootTabComponents()

    #     # Add tabs to widget
    #     self.layout.addWidget(self.tabs)
    #     self.setLayout(self.layout)
        
    # # Create tab Controller
    # def ControllerTabComponents(self):
    #     self.PyQt5_btn = QPushButton("PyQt5 button")
    #     self.PyQt5_btn.clicked.connect(self.on_click)
    #     self.tabController.layout.addWidget(self.PyQt5_btn)
    #     self.tabController.setLayout(self.tabController.layout)

    # def RootTabComponents(self):
    #     self.exitButton = QPushButton("Exit")
    #     self.exitButton.clicked.connect(self.on_exit_click)
    #     self.tabRoot.layout.addWidget(self.exitButton)
    #     self.tabRoot.setLayout(self.tabRoot.layout)

    # @pyqtSlot()
    # def on_click(self):
    #     print('hello')

    # @pyqtSlot()
    # def on_exit_click(self):
    #     # os.system(cmd)
    #     QCoreApplication.instance().quit()
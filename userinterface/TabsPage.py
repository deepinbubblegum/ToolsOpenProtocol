import os
import sys
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from subprocess import call
from userinterface.GeneralWidget import GeneralWidget
from userinterface.OptionsWidget import OptionsWidget
from userinterface.OverviewWidget import OverviewWidget
from userinterface.AdministratorWidget import AdministratorWidget

class TabsWidget(QWidget):
    def __init__(self, parent):   
        super(TabsWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        # Run this after settings
        # self.lang = getLang(config.get("Main", "language"))
        # Initialize tabs
        Tabs = QTabWidget()   # Create tab holder
        tabOverview = OverviewWidget()
        tabGeneral = GeneralWidget()                 # Tab one
        tabOptions = OptionsWidget()                 # Tab two
        tabAdministrator = AdministratorWidget()           # Tab three

        # Add tabs
        Tabs.addTab(tabOverview, "Overview")
        Tabs.addTab(tabGeneral, "General") #self.lang["tab_1_title"]) # Add "tab1" to the tabs holder "tabs"
        # Tabs.addTab(tabOptions, "Options") #self.lang["tab_2_title"]) # Add "tab2" to the tabs holder "tabs" 
        Tabs.addTab(tabAdministrator, "Administrator") #self.lang["tab_2_title"]) # Add "tab2" to the tabs holder "tabs" 
        layout.addWidget(Tabs)
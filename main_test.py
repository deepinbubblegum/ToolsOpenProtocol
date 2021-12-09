#!/usr/bin/python3
import sys
import os
import time
import serial
import numpy as np
from threading import Thread
from system.OpenProtocol import OpenProtocol
from system.cmd_OpenProtocol import cmd_OpenProtocol
from model.SQLControler import sqlControler
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt_material import apply_stylesheet
from userinterface.TabsPage import TabsWidget
from lib.traySocket_v2 import TrayModbusV2
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

class ctl_core():
    def __init__(self, ip_address, port):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.tools_id = port - 9000
        
        self.tray_modbus = None
        
        # init
        self.res_vin_code = None
        
        self.linking_group_data = None
        
        # OpenProtocol
        self._open_cmd = cmd_OpenProtocol()
        self._open_pro = OpenProtocol(self.ip_address, self.port)
        
        # init_disable
        # self._open_pro.send_msg(self._open_cmd.Disable_tool())
        # time.sleep(1)
        
        self.thr_tool = Thread(target=self._tool_sys)
        self.thr_tool.daemon = True
        # self.thr_tool.start()

    def _tool_sys(self):
        while True:
            try:
                if self.linking_group_data is None:
                    self.linking_group_data = self.getLinking_Group_Info()
                else:
                    self.last_tightening_result()
                    print(self.tools_id," : GET LAST RES")
                #print(self.tools_id," : GET INFO")
                time.sleep(1)
            except Exception as err:
                print("ERR")
                pass

    def getInfo(self):
        data = self.linking_group_data
        self.linking_group_data = None
        return data
            
    def getLinking_Group_Info(self):
        try:
            if self._open_pro.send_msg(self._open_cmd.Linking_Group_info_subscribe()):
                return self._open_pro.getLinking_Group_Info()
        except Exception as err:
            pass
        return None
    
    def getTools_ready(self):
        return self.tools_id, self.res_vin_code
    
    def setTools_ack(self):
        self._open_pro.Set_VIN_Number_CODE(None)
        # self.res_vin_code = None
        
    def getTool_link(self):
        return self._open_pro.getSelectLink()
   
    def last_tightening_result(self):
        try:
            self._open_pro.send_msg(self._open_cmd.Last_tightening_result_data_subscribe())
            return self._open_pro.GetData()
        except Exception as err:
            pass
        return ""
    
    def last_tight_none(self):
        self._open_pro.SetData(None)
        
    def disableTool(self):
        try:
            self._open_pro.send_msg(self._open_cmd.Disable_tool())
        except Exception as err:
            pass
        
    def enableTool(self):
        try:
            self._open_pro.send_msg(self._open_cmd.Enable_tool())
        except Exception as err:
            pass
                    
def IP_SQLtxt():
    SQLtxt = 'SELECT IP_Address FROM IP'
    return SQLtxt

def PORT_SQLtxt():
    SQLtxt = 'SELECT PORT_Tools FROM Tools'
    return SQLtxt    

def socket_link_SQLtxt(tool, link):
    SQLtxt = 'SELECT Socket_ID_Step FROM Step WHERE Step_Tools_ID = {} AND ID_Link_step = {} GROUP BY Socket_ID_Step'.format(tool, link)
    return SQLtxt

def step_link_SQLtxt(tool, link):
    SQLtxt = 'SELECT ID_TRAY_ID, Socket_ID_Step FROM Step WHERE Step_Tools_ID = {} AND ID_Link_step = {} ORDER BY Step_number ASC'.format(tool, link)
    return SQLtxt

def findTools(Tools):
    Tools_key = []
    for key, vin in Tools.items():
        if vin is not None:
            Tools_key.append(key)
    return Tools_key

class Worker(QObject):
    complete = pyqtSignal()
    controllerConnect = pyqtSignal(bool)
    socketTotal = pyqtSignal(int)
    socketWarning = pyqtSignal(int)
    socketWarningId = pyqtSignal(str)
    
    @pyqtSlot()
    def runing_thread_worker(self):
        ######### process backgroundworker ########
        self.complete.emit() 

class VLine(QFrame):
    # a simple VLine, like the one you get from designer
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine|self.Sunken)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # this will hide the title bar
        # self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlags(
           Qt.Window |
           Qt.CustomizeWindowHint |
           Qt.WindowShadeButtonHint |
           Qt.WindowMinMaxButtonsHint|
           Qt.WindowTitleHint |
           Qt.WindowCloseButtonHint |
           Qt.WindowStaysOnTopHint
        )

        self.setWindowTitle("GUI Manager OpenProtocal")
        self.setGeometry(100, 100, 720, 480)
        self.setWindowIcon(QIcon('icons/qt.png'))
        
        # calling method
        self.UiStatusBar()
        self.UiComponents()

    # method for widgets
    def UiComponents(self):
        self.tabs_widget = TabsWidget(self)
        self.setCentralWidget(self.tabs_widget)
        
    def UiStatusBar(self):
        self.statusBar().showMessage("STATUS")
        self.ControllerConnect = QLabel("Controller: NO")
        self.ControllerConnect.setStyleSheet('border: 0; color: red;')
        
        self.SocketTotal = QLabel("Total Socket: None")
        self.SocketTotal.setStyleSheet('border: 0; color: blue;')
        
        self.SocketWarning = QLabel("Total Warning: None")
        self.SocketWarning.setStyleSheet('border: 0; color: orange;')
        
        self.SocketWarningID = QLabel("Warning ID: None")
        self.SocketWarningID.setStyleSheet('border: 0; color: red;')
        
        self.statusBar().setStyleSheet('border: 0; background-color: #FFF8DC; margin: 8px;')
        self.statusBar().setStyleSheet("QStatusBar::item {border: none;}") 

        self.statusBar().addPermanentWidget(VLine())    # <---
        self.statusBar().addPermanentWidget(self.ControllerConnect)
        self.statusBar().addPermanentWidget(VLine())    # <---
        self.statusBar().addPermanentWidget(self.SocketTotal)
        self.statusBar().addPermanentWidget(VLine())    # <---
        self.statusBar().addPermanentWidget(self.SocketWarning)
        self.statusBar().addPermanentWidget(VLine())    # <---
        self.statusBar().addPermanentWidget(self.SocketWarningID)
        
    def ControllerConnectStatus(self, status):
        if status:
            self.ControllerConnect.setText("Controller: OK")
            self.ControllerConnect.setStyleSheet('border: 0; color: green;')
        else:
            self.ControllerConnect.setText("Controller: NO")
            self.ControllerConnect.setStyleSheet('border: 0; color: red;') 
        
    def SocketTotalConnect(self, number):
        str_recv = "Total Socket: " + str(number)
        self.SocketTotal.setText(str_recv)
        
    def SocketWarningTotal(self, number):
        str_recv = "Total Warning: " + str(number)
        self.SocketWarning.setText(str_recv)
        
    def SocketWarningIdTotal(self, str):
        str_recv = "Warning ID: " + str
        self.SocketWarningID.setText(str_recv)
        
def handleVisibleChanged():
    if not QGuiApplication.inputMethod().isVisible():
        return
    for w in QGuiApplication.allWindows():
        if w.metaObject().className() == "QtVirtualKeyboard::InputView":
            keyboard = w.findChild(QObject, "keyboard")
            if keyboard is not None:
                r = w.geometry()
                r.moveTop(keyboard.property("y"))
                w.setMask(QRegion(r))
                return
            
@pyqtSlot()
def run_on_complete():
    print('thread ending...')
    
@pyqtSlot()
def updateControllerConnectStatus(val):
    window.ControllerConnectStatus(val) #True / False

@pyqtSlot()
def updateSocketTotalConnect(val):
    window.SocketTotalConnect(val)

@pyqtSlot() 
def updateSocketWarningTotal(val):
    window.SocketWarningTotal(val)

@pyqtSlot() 
def updateSocketWarningIdTotal(val):
    window.SocketWarningIdTotal(val)

def main():
    try:
        global window
        # create the application and the main window
        app = QApplication(sys.argv)
        QGuiApplication.inputMethod().visibleChanged.connect(handleVisibleChanged)
        window = Window()

        extra = {
            'danger': '#dc3545',
            'warning': '#ffc107',
            'success': '#17a2b8',
        }

        apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True, extra=extra)

        # # run
        window.showFullScreen()
        # window.showMaximized()
        
        # instantiate a QThread
        thread = QThread()
        # Instantiate the worker object
        worker = Worker()
        # Relocate the Worker object to the thread
        worker.moveToThread(thread)
        # Connect the 'started' signal of the QThread to the method you wish to run
        thread.started.connect(worker.runing_thread_worker)
        # connect to the 'complete' signal
        worker.complete.connect(run_on_complete)
        worker.controllerConnect.connect(updateControllerConnectStatus)
        worker.socketWarning.connect(updateSocketWarningTotal)
        worker.socketWarningId.connect(updateSocketWarningIdTotal)
        worker.socketTotal.connect(updateSocketTotalConnect)
        # start the thread
        thread.start()
    finally:
        # start the app
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()

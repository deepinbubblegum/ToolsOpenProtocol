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
    
    @pyqtSlot()
    def runing_thread_worker(self):
        linking_group_info = [
            None,None,None,None,
            None,None,None,None,
            None,None,None,None,
            None,None,None,None
        ]
        socket_tray_led_color_pickup = 33
        socket_tray_led_color_picked = 3
        socket_tray_led_color_error = 1
        socket_tray_led_color_return = 11
        socket_tray_led_color_idle = 2
        socket_tray_led_color_off = 0
        socket_tray_enable = [
            False,False,False,False,
            False,False,False,False,
            False,False,False,False,
            False,False,False,False
        ]
        socket_tray_sensor = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        
        socket_tray_led = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        socket_tray_led_prev = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
        ]
        
        # initialize variable
        _port_tools = []
        _tools_pool = []
        Tools = {}
        

        # initialize class
        conn_db = sqlControler(db_file='./database/openprotocol.db')
        
        # Query SQL
        _ip_address = conn_db.db_QuerySQL(IP_SQLtxt())[0][0]
        res_port = conn_db.db_QuerySQL(PORT_SQLtxt())
        for port in res_port:
            print("Port=",port[0])
            _tools_pool.append(ctl_core(ip_address=_ip_address,port=port[0]))
            
        print("Run1")
        tray_modbus = TrayModbusV2(
            port='/dev/ttyS0', 
            device=0x01, 
            baudrate=19200, 
            bytesize = 8, 
            parity=serial.PARITY_NONE, 
            stopbits=1, 
            timeout=1
        )    
        print("Run2")
        
        for _tools in _tools_pool:
            _tools.thr_tool.start()
            time.sleep(0.1)
        
        blink = 0xFFFF
        step_run_prev = [0,0,0,0,0,0,0,0]
        socket_prev = [None,None,None,None,None,None,None,None]
        tray_prev = [None,None,None,None,None,None,None,None]
        tool_enable = [False,False,False,False,False,False,False,False]
        tool_enable_prev = [None,None,None,None,None,None,None,None]
        
        #for tray in range(len(socket_tray_enable)): #Clear LED Off==============================
        for tray in range(1): #Clear LED Off==============================
            for socket in range(8):
                socket_tray_led[tray][socket] = socket_tray_led_color_off
            print(tray)
            tray_modbus.writeSocketTrayLED(tray,list(socket_tray_led[tray]))
            
        print("Run3")
        
        blink = True
        
        while True:
            
            # if blink is True:
            #     blink = False
            # else:
            #     blink = True
                
            time.sleep(0.1)

            #Read Tray Sensor =============================
            for tray in range(len(socket_tray_enable)): 
                if socket_tray_enable[tray] is True:
                    socket_tray_sensor[tray] = tray_modbus.readSocketTraySensor(tray)
                    
            for tray in range(len(socket_tray_enable)): #Clear LED Off==============================
                for socket in range(8):
                    socket_tray_led[tray][socket] = socket_tray_led_color_off
                                
            for _tools in _tools_pool:
                tools_id = _tools.tools_id - 1
                info = _tools.getInfo()
                
                if info is not None:
                    linking_group_info[tools_id] = info
                    tool_enable[tools_id] = False
                    tool_enable_prev[tools_id] = None
                    print("info = " , info)
                    
                linking_group_data = linking_group_info[tools_id]
                if linking_group_data is not None:   
                    linking_group_id = int(linking_group_data['Linking_Group_ID'])
                    linking_group_status = int(linking_group_data['Linking_Group_status'])
                    linking_group_batch_mode = int(linking_group_data['Linking_Group_batch_mode'])
                    linking_group_batch_size = int(linking_group_data['Linking_Group_batch_size'])
                    linking_group_batch_counter = int(linking_group_data['Linking_Group_batch_counter'])
                    #print("tools_id=",tools_id , " ", linking_group_id ," ",linking_group_status," ",linking_group_batch_mode," ",linking_group_batch_size," ",linking_group_batch_counter)

                    res_steps_socket = conn_db.db_QuerySQL(step_link_SQLtxt(tools_id + 1, linking_group_id))
                    
                    step_run = linking_group_batch_counter
                    step_size = linking_group_batch_size
                    
                    # print("Tool ", tools_id ," = ",tool_enable[tools_id] , " " , step_run , " " , step_size)

                    str_step = "0"
                    if step_run == step_size:
                        str_step = "X"
                    else:
                        str_step = str(step_run + 1)
                    
                    if step_run < step_size:
                        try:
                            ss = str(res_steps_socket[step_run][1])
                        except:
                            print('error ss variable invalid')
                    else:
                        ss = "X"
                    
                    try:
                        print("Tools ", tools_id + 1 ," , Enable : ",tool_enable[tools_id] , " , Link : " , linking_group_id , " , Step : ", str_step , " / " , step_size, " , Socket : " , ss)
                        print(res_steps_socket)
                    except :
                        print("out of range " ,step_run )
    
                    db_step_size = len(res_steps_socket)
                    
                    
                    if db_step_size < step_size: #step size no correct
                            
                        for step in range(len(res_steps_socket)):
                            tray = res_steps_socket[step][0] - 1
                            socket = res_steps_socket[step][1] - 1
                            socket_tray_enable[tray] = True #Enable Tray
                            
                            if blink is True:
                                socket_tray_led[tray][socket] = socket_tray_led_color_error
                            else:
                                socket_tray_led[tray][socket] = socket_tray_led_color_off
                                
                        tool_enable[tools_id] = False
                    else:
                        #======================================
                        if step_run < step_size:
                            tray = res_steps_socket[step_run][0] - 1
                            socket = res_steps_socket[step_run][1] - 1
                            
                            if socket_prev[tools_id] is None:
                                socket_prev[tools_id] = socket
                            if tray_prev[tools_id] is None:
                                tray_prev[tools_id] = tray   

                        
                        #SQN Process ==================================
                        if linking_group_status != 0: #Idle          
                            for step in range(len(res_steps_socket)):
                                tray = res_steps_socket[step][0] - 1
                                socket = res_steps_socket[step][1] - 1
                                socket_tray_enable[tray] = True #Enable Tray
                                if socket_tray_sensor[tray][socket] >= 1: #Have Socket
                                    socket_tray_led[tray][socket] = socket_tray_led_color_idle
                                else:
                                    socket_tray_led[tray][socket] = socket_tray_led_color_error
                                    tool_enable[tools_id] = False
                        
                        if linking_group_status == 0: #Run Batch
                            if step_run < step_size:
                                if step_run != step_run_prev[tools_id]:# Check All Socket Ready if not fisrt time
                                    tray = res_steps_socket[step_run][0] - 1
                                    socket = res_steps_socket[step_run][1] - 1  
                                    all_socket_ready = True
                                    
                                    try:
                                            tray_last = res_steps_socket[step_run_prev[tools_id]][0] - 1
                                            socket_last = res_steps_socket[step_run_prev[tools_id]][1] - 1  
                                    except:
                                            pass
                                    
                                    if tray == tray_last and socket == socket_last:
                                        pass
                                    else:
                                        #===============================================
                                        for step in range(len(res_steps_socket)):
                                            tray = res_steps_socket[step][0] - 1
                                            socket = res_steps_socket[step][1] - 1
                                            socket_tray_enable[tray] = True
                                            if socket_tray_sensor[tray][socket] >= 1:# LED Return proc
                                                socket_tray_led[tray][socket] = socket_tray_led_color_idle
                                            else:
                                                tool_enable[tools_id] = False
                                                if blink is True:
                                                    socket_tray_led[tray][socket] = socket_tray_led_color_return
                                                else:
                                                    socket_tray_led[tray][socket] = socket_tray_led_color_off
                                                
                                            if socket_tray_sensor[tray][socket] == 0:#No Socket
                                                all_socket_ready = False 
                                        #===============================================   
                                    if all_socket_ready is True:
                                        a = int(step_run)
                                        step_run_prev[tools_id] = a
                                        
                                if step_run == step_run_prev[tools_id]:#loop Pickup   
                                    for step in range(len(res_steps_socket)):#Set All Idle
                                        tray = res_steps_socket[step][0] - 1
                                        socket = res_steps_socket[step][1] - 1
                                        socket_tray_enable[tray] = True
                                        if socket_tray_sensor[tray][socket] >= 1:
                                            socket_tray_led[tray][socket] = socket_tray_led_color_idle
                                        else:
                                            socket_tray_led[tray][socket] = socket_tray_led_color_error
                                            
                                    tray = res_steps_socket[step_run][0] - 1
                                    socket = res_steps_socket[step_run][1] - 1
                            
                                    if socket_tray_sensor[tray][socket] >= 1:
                                        tool_enable[tools_id] = False
                                        if blink is True:
                                            socket_tray_led[tray][socket] = socket_tray_led_color_pickup
                                        else:
                                            socket_tray_led[tray][socket] = socket_tray_led_color_off
                                    else:
                                        socket_tray_led[tray][socket] = socket_tray_led_color_picked
                                        tool_enable[tools_id] = True
                                        
                                    #ReCheck===========
                                    tray_run = res_steps_socket[step_run][0] - 1
                                    socket_run = res_steps_socket[step_run][1] - 1
                                    
                                    for step in range(len(res_steps_socket)):#Set All Idle
                                        tray = res_steps_socket[step][0] - 1
                                        socket = res_steps_socket[step][1] - 1
                                        if tray_run == tray and socket_run == socket:
                                            pass
                                        else:
                                            if socket_tray_sensor[tray][socket] == 0:
                                                tool_enable[tools_id] = False
    


                
            
                #Tool Control =================================
                bypass_tool_id = tools_id + 1
                res_bypass = conn_db.db_get_bypass_tool(bypass_tool_id)
                if bool(res_bypass) == True:
                    tool_enable[tools_id] = True
    
                if tool_enable[tools_id] != tool_enable_prev[tools_id]:
                    a = bool(tool_enable[tools_id])
                    tool_enable_prev[tools_id] = a
                    if bool(res_bypass) == True:
                        print(" tool ", tools_id + 1, " ByPassTool")
                    
                    if tool_enable[tools_id] is True:
                        try:
                            _tools.enableTool()
                            print(" tool ", tools_id + 1, " enableTool")
                        except:
                            print("enableTool error")
                            pass
                    else:
                        try:
                            _tools.disableTool()
                            print(" tool ", tools_id + 1, " disableTool")
                        except:
                            print("disableTool error")
                            pass

                        
            #Write Tray Led ===============================
            for tray in range(len(socket_tray_enable)):   
                if socket_tray_enable[tray] is True:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    
                    for i in range(8):
                        linking_group_data = linking_group_info[i]
                        if linking_group_data is not None:   
                            linking_group_batch_size = int(linking_group_data['Linking_Group_batch_size'])
                            linking_group_batch_counter = int(linking_group_data['Linking_Group_batch_counter'])
    
                            step_run = linking_group_batch_counter
                            step_size = linking_group_batch_size

                            # print("Tools ", i + 1 ," = ",tool_enable[i] , " " , step_run + 1 , " " , step_size, " " , res_steps_socket[step_run][1])

                    print(current_time)
                    print("PROX > 1 = Socket Detect / 0 = No Socket")
                    print("{:02X} , {:02X} , {:02X} , {:02X}".format(socket_tray_sensor[tray][0],socket_tray_sensor[tray][1],socket_tray_sensor[tray][2],socket_tray_sensor[tray][3]))
                    print("{:02X} , {:02X} , {:02X} , {:02X}".format(socket_tray_sensor[tray][4],socket_tray_sensor[tray][5],socket_tray_sensor[tray][6],socket_tray_sensor[tray][7]))
                    print("LED > 11 = Return | 1 = NoSocket | 3 = Picked | 33 = Pickup | 2 = Normal")
                    print("{:02X} , {:02X} , {:02X} , {:02X}".format(socket_tray_led[tray][0],socket_tray_led[tray][1],socket_tray_led[tray][2],socket_tray_led[tray][3]))
                    print("{:02X} , {:02X} , {:02X} , {:02X}".format(socket_tray_led[tray][4],socket_tray_led[tray][5],socket_tray_led[tray][6],socket_tray_led[tray][7]))
                    print("==============================")
                        
                    if list(socket_tray_led_prev[tray]) != list(socket_tray_led[tray]):
                        #print(tray," write = ",socket_tray_led[tray])
                        tray_modbus.writeSocketTrayLED(tray,list(socket_tray_led[tray]))
                        a = list(socket_tray_led[tray])
                        socket_tray_led_prev[tray] = a
        self.complete.emit() 

@pyqtSlot()
def run_on_complete():
    print('thread ending...')

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

        self.setWindowTitle("GUI Manager")
        self.setGeometry(100, 100, 720, 480)
        self.setWindowIcon(QIcon('icons/qt.png'))

        # calling method
        self.UiComponents()

    # method for widgets
    def UiComponents(self):
        self.tabs_widget = TabsWidget(self)
        self.setCentralWidget(self.tabs_widget)

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

def main():
    try:
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
        # start the thread
        thread.start()
    finally:
        # start the app
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()

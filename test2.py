#!/usr/bin/python3
import time
import serial
import sqlite3
from threading import Thread
from system.OpenProtocol import OpenProtocol
from system.cmd_OpenProtocol import cmd_OpenProtocol
from model.SQLControler import sqlControler
import numpy as np
from lib.traySocket_v2 import TrayModbusV2





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
        time.sleep(1)
        
        self.thr_tool = Thread(target=self._tool_sys)
        self.thr_tool.daemon = True
        # self.thr_tool.start()


    def _tool_sys(self):
        while True:
            if self.linking_group_data is None:
                self.linking_group_data = self.getLinking_Group_Info()
            time.sleep(0.1)
     

    def getInfo(self):
        data = self.linking_group_data
        self.linking_group_data = None
        return data
            
    def getLinking_Group_Info(self):
        if self._open_pro.send_msg(self._open_cmd.Linking_Group_info_subscribe()):
            return self._open_pro.getLinking_Group_Info()
        return None
    
    def getTools_ready(self):
        return self.tools_id, self.res_vin_code
    
    def setTools_ack(self):
        self._open_pro.Set_VIN_Number_CODE(None)
        # self.res_vin_code = None
        
    def getTool_link(self):
        return self._open_pro.getSelectLink()
   
    def last_tightening_result(self):
        self._open_pro.send_msg(self._open_cmd.Last_tightening_result_data_subscribe())
        return self._open_pro.GetData()
    
    def last_tight_none(self):
        self._open_pro.SetData(None)
        
    def disableTool(self):
        self._open_pro.send_msg(self._open_cmd.Disable_tool())
        
    def enableTool(self):
        self._open_pro.send_msg(self._open_cmd.Enable_tool())
                    
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
        
        
def main():
    linking_group_info = [
        None,None,None,None,
        None,None,None,None,
        None,None,None,None,
        None,None,None,None
    ]
    socket_tray_led_color_pickup = 0x0F0
    socket_tray_led_color_picked = 0x0F0
    socket_tray_led_color_error = 0xF00
    socket_tray_led_color_return = 0xF00
    socket_tray_led_color_idle = 0x2F0
    socket_tray_led_color_off = 0x000
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
        port='/dev/ttyUSB0', 
        device=0x01, 
        baudrate=9600, 
        bytesize = 8, 
        parity=serial.PARITY_NONE, 
        stopbits=1, 
        timeout=0.5
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
    
    for tray in range(len(socket_tray_enable)): #Clear LED Off==============================
        for socket in range(8):
            socket_tray_led[tray][socket] = socket_tray_led_color_off
        print(tray)
        tray_modbus.writeSocketTrayLED(tray,list(socket_tray_led[tray]))
        
    print("Run3")
    
    while True:
        
        if blink is True:
            blink = False
        else:
            blink = True
            
        # time.sleep(0.1)

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

                                tray_last = res_steps_socket[step_run_prev[tools_id]][0] - 1
                                socket_last = res_steps_socket[step_run_prev[tools_id]][1] - 1  
                                
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
            if tool_enable[tools_id] != tool_enable_prev[tools_id]:
                a = bool(tool_enable[tools_id])
                tool_enable_prev[tools_id] = a
                if tool_enable[tools_id] is True:
                    _tools.enableTool()
                    print(" tool ", tools_id + 1, " enableTool")
                else:
                    _tools.disableTool()
                    print(" tool ", tools_id + 1, " disableTool")
                    
        #Write Tray Led ===============================
        for tray in range(len(socket_tray_enable)):   
            if socket_tray_enable[tray] is True:            
                if list(socket_tray_led_prev[tray]) != list(socket_tray_led[tray]):
                    print(tray," write = ",socket_tray_led[tray])         
                    tray_modbus.writeSocketTrayLED(tray,list(socket_tray_led[tray]))
                    a = list(socket_tray_led[tray])
                    socket_tray_led_prev[tray] = a
         
                
        
        # for tray in range(len(socket_tray_enable)):
        #     if socket_tray_enable[tray] is True:
        #         socket_tray_input[tray] = list(tray_modbus.readSocketTraySensor(tray))
                
                
                  
        # for tray in range(len(socket_tray_enable)):   
        #     if socket_tray_enable[tray] is True:   
        #         print(tray," read = ",socket_tray_input[tray])
        #         print(tray," led = ",socket_tray_led[tray])  
        #         print(tray," prev = ",socket_tray_led_prev[tray])     
        #         if socket_tray_led_prev[tray] != socket_tray_led[tray]:
        #             print(tray," write = ",socket_tray_led[tray])         
        #             tray_modbus.writeSocketTrayLED(tray,list(socket_tray_led[tray]))
        #             socket_tray_led_prev[tray] = socket_tray_led[tray]
         
        #         print(tray," prev2 = ",socket_tray_led_prev[tray])             
                    
        # _socket_tray_input = socket_tray_input
        
        # print("tray = ",socket_tray_enable)      
        
        # tray_modbus.writeSocketTrayLED(0,[0xF00,0xF00,0xF00,0xF00,0xF00,0xF00,0xF00,0xF00])
        # time.sleep(0.25)
        # tray_modbus.writeSocketTrayLED(0,[0x000,0x000,0x000,0x000,0x000,0x000,0x000,0x000])
        # time.sleep(0.25)
        # if tools_init is not None:
        #     # print(tools_init)
        #     #_tools_pool[tools_init-1].set_tray_modbus(tray_modbus)
        #     _tools_pool[tools_init-1].setTools_ack()
        #     Linking_ID = _tools_pool[tools_init-1].getTool_link()['Linking_Group_ID']
        #     # print(res['Linking_Group_ID'])
        #     res_socket_list = conn_db.db_QuerySQL(socket_link_SQLtxt(tools_init, Linking_ID))
        #     # for socket in res_socket_list:
        #     #     tray_modbus.setEnable(int(socket[0])-1)
        #     res_steps_socket = conn_db.db_QuerySQL(step_link_SQLtxt(tools_init, Linking_ID))
        #     _tools_pool[tools_init-1].last_tight_none()
        #     while True:
        #         print('Start Loop')
        #         loop = len(res_steps_socket)
        #         try:
        #             res_steps_socket[checked][1]
        #         except Exception as e:
        #             break
            
        #         if loop == checked:
        #             checked = 0
        #             print('exit loop')
        #             break
                
        #         # tray_modbus.pick_id((res_socket_list[checked][0])-1)
        #         print(res_socket_list[checked][0]-1)
                
        #         res_last_tigh = _tools_pool[tools_init-1].last_tightening_result()
                
        #         # if tray_modbus.get_socket_ready():
        #         #     _tools_pool[tools_init-1].enableTool()
        #         # else:
        #         #     _tools_pool[tools_init-1].disableTool()
                    
        #         if res_last_tigh is not None:
        #             if int(res_last_tigh['Tightening_Status']):
        #                 #_tools_pool[tools_init-1].disableTool()
        #                 checked += 1
        #                 print('Tightening :OK')
        #             else:
        #                 print('Tightening :NOK')
        #                 if old_position != res_last_tigh['Batch_counter']:
        #                     #_tools_pool[tools_init-1].disableTool()
        #                     checked += 1
        #                     # _tools_pool[tools_init-1].set_NextPosition()
        #             old_position = res_last_tigh['Batch_counter']
        #             _tools_pool[tools_init-1].last_tight_none()
        #         time.sleep(0.01)
        #     # tray_modbus.pick_id(-1)
        #     print('end cycle position')
        # time.sleep(0.01)
    
if __name__=='__main__':
    main()

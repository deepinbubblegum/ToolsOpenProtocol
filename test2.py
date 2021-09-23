#!/usr/bin/python3
import time
import serial
import sqlite3
from threading import Thread
from system.OpenProtocol import OpenProtocol
from system.cmd_OpenProtocol import cmd_OpenProtocol
from model.SQLControler import sqlControler
# from lib.traySocket_v2 import TrayModbusV2

class ctl_core():
    def __init__(self, ip_address, port):
        super().__init__()
        self.ip_address = ip_address
        self.port = port
        self.tools_id = port - 9000
        
        self.tray_modbus = None
        
        # init
        self.res_vin_code = None
        
        # OpenProtocol
        self._open_cmd = cmd_OpenProtocol()
        self._open_pro = OpenProtocol(self.ip_address, self.port)
        
        # init_disable
        self._open_pro.send_msg(self._open_cmd.Disable_tool())
        
        self.thr_tool = Thread(target=self._tool_sys)
        self.thr_tool.daemon = True
        self.thr_tool.start()

    def _tool_sys(self):
        while True:
            self._open_pro.send_msg(self._open_cmd.Linking_Group_info_subscribe())
            time.sleep(0.02)
            if self._open_pro.send_msg(self._open_cmd.Vehicle_Id_Number_upload_subscribe()) is True:
                self.res_vin_code = self._open_pro.Get_VIN_Number_CODE()
                if self.res_vin_code is None:
                    continue
            time.sleep(1)
            
    def getTools_ready(self):
        return self.tools_id, self.res_vin_code
    
    def setTools_ack(self):
        self._open_pro.Set_VIN_Number_CODE(None)
        self.res_vin_code = None
        
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

def thr_socket_step(_tool):
    pass
    
def main():
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
        _tools_pool.append(ctl_core(
            ip_address=_ip_address,
            port=port[0]
            )
        )
    
    # oparations
    while True:
        thr_tools_pool = []
        for _tools in _tools_pool:
            tools_id, res_vin_code = _tools.getTools_ready()
            if res_vin_code is not None:
                Tools[tools_id] = res_vin_code
                time.sleep(0.02)  
        tools_init = findTools(Tools)
        if len(tools_init) > 0:
            # start thr
            thr_tools_pool.append(
                Thread(target=thr_socket_step, args=(_tools_pool[tools_init-1],))
            )
            thr_tools_pool[tools_init-1].daemon = True
            thr_tools_pool[tools_init-1].start()
            _tools_pool[tools_init-1].setTools_ack()
        time.sleep(0.01)
        
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

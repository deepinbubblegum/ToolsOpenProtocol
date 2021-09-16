from threading import Thread
import threading
import time
import serial
import sqlite3
from model.SQLControler import sqlControler
from cmd_OpenProtocol import cmd_OpenProtocol
from OpenProtocol import OpenProtocol
from socket_tray import socket_tray
# from lib.traySocket_v2 import TrayModbusV2

class SystemControllers():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.tools_id = port - 9000
        self.res_VIN_CODE = None
        
        self.OpenProtocol = OpenProtocol(self.ip_address, self.port)
        self.cmd = cmd_OpenProtocol()
        
        # init_disable
        while True:
            if self.OpenProtocol.send_msg(self.cmd.Disable_tool()) is not True:
                time.sleep(0.2)
                continue
            break
        
        self.thr_tool = Thread(target=self._tool_sys)
        self.thr_tool.daemon = True
        self.thr_tool.start()
    
    def _tool_sys(self):
        while True:
            self.OpenProtocol.send_msg(self.cmd.Linking_Group_info_subscribe())
            time.sleep(0.02)
            if self.OpenProtocol.send_msg(self.cmd.Vehicle_Id_Number_upload_subscribe()) is True:
                res_VIN_CODE = self.OpenProtocol.Get_VIN_Number_CODE()
                if res_VIN_CODE is None:
                    continue
                self.res_VIN_CODE = res_VIN_CODE
            time.sleep(1)
            
    def getTools_ready(self):
        tools_id = self.tools_id
        res_VIN_CODE = self.res_VIN_CODE
        self.tools_id = None
        self.res_VIN_CODE = None
        return tools_id, res_VIN_CODE
    
    def getTools_link(self):
        link_group_select = self.OpenProtocol.Get_link_group_select()
        self.OpenProtocol.Set_link_group_select = None
        return link_group_select
    
    def SetEnable(self):
        self.OpenProtocol.send_msg(self.cmd.Enable_tool())
    
    def setTools_ack(self):
        self.res_VIN_CODE = None
    
def main():
    _ip_address = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008
    ]
    
    db = sqlControler('../database/openprotocol.db')
    _Controller_pool = []
    tools_id = None
    res_VIN_CODE = None
    for _port_tool in PORT_TOOL:
        _Controller_pool.append(SystemControllers(_ip_address, _port_tool))
        
    while True:
        if res_VIN_CODE is None:
            for _Contorller in _Controller_pool:
                tools_id, res_VIN_CODE = _Contorller.getTools_ready()
                if res_VIN_CODE is not None:
                    break
                time.sleep(0.2)
        while True:
            checked = 0
            old_position = None
            if res_VIN_CODE is not None:
                # print(tools_id, res_VIN_CODE)
                link_group = _Controller_pool[tools_id - 1].getTools_link()
                if link_group is not None:
                    print(link_group)
                    SQL_txt = 'SELECT Socket_ID_Step FROM Step WHERE Step_Tools_ID = {} AND ID_Link_step = {} GROUP BY Socket_ID_Step'.format(tools_id, link_group['Linking_Group_ID'])
                    res_socket_tray = db.db_QuerySQL(SQL_txt)
                    for res in res_socket_tray:
                        print(res)
                    if tools_id is not None:
                        _Controller_pool[tools_id - 1].SetEnable()
                    # SQL_txt = 'SELECT * FROM Step WHERE ID_Link_step = 1 ORDER BY Step_number ASC'
                    # res_step = QuerySQL(SQL_txt)
            else:
                break
            

if __name__ == '__main__':
    main()
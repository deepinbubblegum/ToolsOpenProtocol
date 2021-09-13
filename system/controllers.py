from threading import Thread
import time
import serial
import sqlite3
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
        return self.tools_id, self.res_VIN_CODE
    
    def setTools_ack(self):
        self.res_VIN_CODE = None
          
def main():
    _ip_address = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008
    ]
    _Controller_pool = []
    Controller = {}
    for _port_tool in PORT_TOOL:
        _Controller_pool.append(SystemControllers(_ip_address, _port_tool))
        time.sleep(1)
        
    while True:
        while True:
            for _Contorller in _Controller_pool:
                tools_id, res_VIN_CODE = _Contorller.getTools_ready()
                Controller[tools_id] = res_VIN_CODE
                time.sleep(0.5)
            print(Controller)

if __name__ == '__main__':
    main()
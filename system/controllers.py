from threading import Thread
import time
import serial
import sqlite3
from system.cmd_OpenProtocol import cmd_OpenProtocol
from system.OpenProtocol import OpenProtocol
from system.socket_tray import socket_tray
from lib.traySocket_v2 import TrayModbusV2

class SystemControllers():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        
        self.OpenProtocol = OpenProtocol(self.ip_address, self.port)
        self.cmd = cmd_OpenProtocol()
        
        # init_disable
        while True:
            if open.send_msg(self.cmd.Disable_tool()) is not True:
                time.sleep(0.2)
                continue
            break
        
        self.thr_tool = Thread(target=self._tool_sys)
        self.thr_tool.daemon = True
        self.thr_tool.start()
    
    def _tool_sys(self):
        while True:
            self.OpenProtocol.send_msg(self.Linking_Group_info_subscribe())
            if open.send_msg(self.cmd.Vehicle_Id_Number_upload_subscribe()) is True:
                res_VIN_CODE = open.Get_VIN_Number_CODE()
                if res_VIN_CODE is None:
                    continue
                print(res_VIN_CODE)
            time.sleep(0.2)
          
def main():
    HOST = '10.1.10.22'
    PORT_TOOL = [
        9001, 9002, 9003, 9004,
        9005, 9006, 9007, 9008
    ]
    _Controller1 = SystemControllers()
    _Controller2 = SystemControllers()
    _Controller3 = SystemControllers()
    _Controller4 = SystemControllers()
    _Controller5 = SystemControllers()
    _Controller6 = SystemControllers()
    _Controller7 = SystemControllers()
    _Controller8 = SystemControllers()
    

if __name__ == '__main__':
    main()
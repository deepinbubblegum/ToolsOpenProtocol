import threading
import time
from system.cmd_OpenProtocol import cmd_OpenProtocol

class socket_tray():
    def __init__(self, tray_modbus, open):
        self.open = open
        self.tray_modbus = tray_modbus
        self.cmd = cmd_OpenProtocol()
        
        self.NextPosition = False
        self.picked_socket = False
        self.drop_socket = True
        self.pick_id = None
        self.old_pick_id = None
        
        self.thr_tray = threading.Thread(target=self.thr_socket_tray)
        self.thr_tray.daemon = True
        self.thr_tray.start()

    def thr_socket_tray(self):
        while True:
            res_socket = self.tray_modbus.get_socket_pickup()
            if self.NextPosition is True:
                if self.pick_id is not None and bool(res_socket[self.pick_id - 1]):
                    if self.old_pick_id is not None and bool(res_socket[self.old_pick_id - 1]):
                        self.open.send_msg(self.cmd.Disable_tool())
                    else:
                        self.open.send_msg(self.cmd.Enable_tool())
                else:
                    self.open.send_msg(self.cmd.Disable_tool())
                    self.NextPosition = False    
            
    def set_socket_pickup(self, hole):
        self.tray_modbus.set_socket_pickup(hole)
        self.NextPosition = True
        self.pick_id = hole
        
    def set_NextPosition(self):
        self.NextPosition = True
        self.old_pick_id = self.pick_id
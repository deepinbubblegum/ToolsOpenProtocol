#!/usr/bin/env python3
from socket import socket
import minimalmodbus
import serial
import time
import threading

class TrayModbusV2():
    def __init__(self, port='/dev/ttyUSB0', device=0x01, baudrate=19200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1):
        self.modbus = [
            minimalmodbus.Instrument(port, 1), 
            minimalmodbus.Instrument(port, 2),
            minimalmodbus.Instrument(port, 3),
            minimalmodbus.Instrument(port, 4),
            minimalmodbus.Instrument(port, 5),
            minimalmodbus.Instrument(port, 6),
            minimalmodbus.Instrument(port, 7),
            minimalmodbus.Instrument(port, 8)
        ]
        
        self.modbus[0].serial.baudrate = baudrate         # Baud
        self.modbus[0].serial.bytesize = bytesize
        self.modbus[0].serial.parity = parity
        self.modbus[0].serial.stopbits = stopbits
        self.modbus[0].serial.timeout = timeout          # seconds
        self.modbus[0].mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        self.modbus[0].clear_buffers_before_each_transaction = True
        for i in range(8):
            self.modbus[i] = minimalmodbus.Instrument(port, i+1)
            
        self.socket_pickup = None
        self.bing_picked = False

        self.socket_tray_check_obj = False
        self.tray_enable = [0,0,0,0,0,0,0,0]
        self.socket_enable = [8][0,0,0,0,0,0,0,0]
        self.socket_tray_sensor = [8][
            0,0,0,0,
            0,0,0,0
        ]

        self.leds_socket_tray = [8][
            0x000,0x000,0x000,0x000,
            0x000,0x000,0x000,0x000
        ]
        
        self.leds_socket_tray_prev = [8][
            0x000,0x000,0x000,0x000,
            0x000,0x000,0x000,0x000
        ]

        self.socket_ready[8] = False
        self.socket_get[8] = [-1,-1,-1,-1,-1,-1,-1,-1]
        
        self.led_color_disable = 0x000
        self.led_color_enable = 0xFF0
        self.led_color_error = 0xF00
        self.led_color_pickup = 0x00F
        self.led_color_picked = 0x0F0
    
        self.color_rgb = [0xF00, 0x0F0, 0x00F, 0x000]
        self.list_set = []
        
        self.thread_event_socket = threading.Thread(target=self.event_socket_tray)
        self.thread_event_socket.daemon = True
        self.thread_event_socket.start()
        
        self.thread_tray_socket = threading.Thread(target=self.Thread_Tray_socket)
        self.thread_tray_socket.daemon = True
        self.thread_tray_socket.start()
        
        self.thread_tray_socket_led = threading.Thread(target=self.Thread_Tray_socket_led)
        self.thread_tray_socket_led.daemon = True
        self.thread_tray_socket_led.start()
        
    def Thread_Tray_socket_led(self):
        while True:
            self.led_color_pickup = 0x0F0
            time.sleep(0.25)
            self.led_color_pickup = 0x000
            time.sleep(0.25)
            
    def readSocketTraySensor(self,id):
        socket_tray_data = [-1,-1,-1,-1,-1,-1,-1,-1]
        try:
            socket_tray_data = self.modbus[id].read_registers(0,8,4)
        except Exception as e:
            print(e)
        return socket_tray_data
    
    def writeSocketTrayLED(self,id,data):
        try:
            self.modbus[id].write_registers(0, data)
        except Exception as e:
            print(e)
    
    def Thread_Tray_socket(self):
        while True:
            for i in range(8):
                if self.tray_enable[i] >= 1:
                    self.socket_tray_sensor[i] = self.readSocketTraySensor(i)
            
            for i in range(8):
                if self.tray_enable[i] >= 1:
                    if self.leds_socket_tray[i] != self.leds_socket_tray_prev[i]:
                        self.leds_socket_tray_prev[i] =self.leds_socket_tray[i]
                        self.writeSocketTrayLED(id,self.leds_socket_tray[i])

    def event_socket_tray(self):
        while True:
            all_socket_ready = True
            for i in range(8):
                # print('Enable',self.socket_enable)
                # print('Sensor',self.socket_tray)
                if self.socket_enable[i] == 1: 
                    if self.socket_tray[i] == 0:
                        # print('socket active {}'.format(i))
                        self.leds_socket_tray[i] = self.led_color_enable
                    else:
                        if self.socket_get != i:
                            self.leds_socket_tray[i] = self.led_color_error
                            all_socket_ready = False     
                else:
                    self.leds_socket_tray[i] = self.led_color_disable
                    
            if all_socket_ready is True:
                if self.socket_get >= 0 and self.socket_get < 8:
                    if self.socket_tray[self.socket_get] == 1:
                        self.leds_socket_tray[self.socket_get] = self.led_color_picked
                        self.socket_ready = True
                    else:
                        self.leds_socket_tray[self.socket_get] = self.led_color_pickup
                        self.socket_ready = False
                else:
                    self.socket_ready = False
            else:
                self.socket_ready = False
            # print('Commnd',self.leds_socket_tray)
            time.sleep(0.1)
         
    def set_socket_pickup(self, value):
        self.socket_pickup = value   
        
    def get_socket_pickup(self):
        return self.socket_tray
    
    def get_tray_enable(self):
        return self.tray_enable
    
    def get_socket_enable(self):
        return self.socket_enable
    
    def set_tray_enable(self, value):
        self.tray_enable = value
    
    def set_socket_enable(self, value):
        self.socket_enable = value
      
    def setledOn_formDB(self, idx):
        self.list_set.append(idx)
        self.leds_socket_tray[idx] = 0xF00
        
    def setledOn_reset(self):
        self.list_set = []
        
    def read_registers(self, registeraddress, numberOfDecimals = 0, functioncode = 4):
        registervalue = self.instrument.read_registers(
            registeraddress,
            numberOfDecimals,
            functioncode
        )
        return registervalue
    
    def setEnable(self, idx):
        self.socket_enable[idx] = 1
        
    def setDisable(self, idx):
        self.socket_enable[idx] = 0
        
    def get_socket_ready(self):
        return self.socket_ready
    
    def pick_id(self, val):
        self.socket_get = val
    
    def write_registers(self, registeraddress, value):
        self.instrument.write_registers(registeraddress, value)
        
# def main():
#     tray_modbus = TrayModbusV2(
#         port='/dev/ttyUSB0', 
#         device=0x01, 
#         baudrate=19200, 
#         bytesize = 8, 
#         parity=serial.PARITY_NONE, 
#         stopbits=1, 
#         timeout=0.05
#     )
#     while True:
#         time.sleep(1)
    

# if __name__=='__main__':
#     main()
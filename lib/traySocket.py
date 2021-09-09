#!/usr/bin/env python3
import minimalmodbus
import serial
import time
import threading

class TrayModbus():
    def __init__(self, port='/dev/ttyUSB0', device=0x01, baudrate=19200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=1):
        self.instrument = minimalmodbus.Instrument(
            port, device)  # port name, slave address (in decimal)
        self.instrument.serial.port                     # this is the serial port name
        self.instrument.serial.baudrate = baudrate         # Baud
        self.instrument.serial.bytesize = bytesize
        self.instrument.serial.parity = parity
        self.instrument.serial.stopbits = stopbits
        self.instrument.serial.timeout = timeout          # seconds

        # this is the slave address number
        self.instrument.address
        self.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        self.instrument.clear_buffers_before_each_transaction = True

        self.socket_pickup = None
        self.bing_picked = False

        self.socket_tray_check_obj = False
        self.socket_tray = [
            0,0,0,0,
            0,0,0,0
        ]
        
        self.leds_socket_tray = [
            0x000,0x000,0x000,0x000,
            0x000,0x000,0x000,0x000
        ]
        
        self.color_rgb = [0xF00, 0x0F0, 0x00F, 0x000]
        self.color_g_bing = [0x000, 0x0F0]
        
        self.thread_tray_socket = threading.Thread(target=self.Thread_Tray_socket)
        self.thread_tray_socket.daemon = True
        self.thread_tray_socket.start()
        
        self.thread_event_socket = threading.Thread(target=self.event_socket_tray)
        self.thread_event_socket.daemon = True
        self.thread_event_socket.start()

    def Thread_Tray_socket(self):
        while True:
            for idx_add in range(len(self.socket_tray)):
                try:
                    self.socket_tray[idx_add] = self.read_register(
                        registeraddress = idx_add,
                        numberOfDecimals = 0,
                        functioncode = 4,
                        signed = False
                    )
                    self.write_register(
                        registeraddress=idx_add, 
                        value=self.leds_socket_tray[idx_add],
                        mode=0
                    )
                except Exception as e:
                    pass
                
    def event_socket_tray(self):
        idx_bing_led = 0
        while True:
            for idx in range(len(self.socket_tray)):
                if bool(self.socket_tray[idx]) is False and (idx + 1) != self.socket_pickup:
                    self.leds_socket_tray[idx] = self.color_rgb[2]
                elif bool(self.socket_tray[idx]) is False and (idx + 1) == self.socket_pickup:
                    self.leds_socket_tray[idx] = self.color_rgb[1]
                elif bool(self.socket_tray[idx]) and (idx + 1) == self.socket_pickup:
                    self.leds_socket_tray[idx] = self.color_g_bing[idx_bing_led]
                elif bool(self.socket_tray[idx]) and (idx + 1) != self.socket_pickup:
                    self.leds_socket_tray[idx] = self.color_rgb[0]  
            if idx_bing_led >= 1:
                idx_bing_led = 0
            else:
                idx_bing_led += 1
            time.sleep(0.25)

    def set_socket_pickup(self, value):
        self.socket_pickup = value
        
    def get_socket_pickup(self):
        return self.socket_tray
        
    def write_register(self, registeraddress, value, mode=0):
        self.instrument.write_register(registeraddress, value, mode)

    def read_register(self, registeraddress, mode=0):
        res_value = self.instrument.read_register(
            registeraddress, 
            mode
        )  # Registernumber, number of decimals
        return hex(res_value)
    
    def read_register(self, registeraddress, numberOfDecimals = 0, functioncode = 4, signed = False):
        registervalue = self.instrument.read_register(
            registeraddress,
            numberOfDecimals,
            functioncode,
            False
        )
        return registervalue

    def close(self):
        self.instrument.serial.close()
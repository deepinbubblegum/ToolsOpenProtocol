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

        self.socket_pickup = 1
        self.bing_picked = False

        self.socket_tray_check_obj = False
        self.socket_tray = {
            1: 1, 2: 1, 3: 1, 4: 1,
            5: 1, 6: 1, 7: 1, 8: 1,
        }
        
        self.color_rgb = [0x0F0, 0x000, 0x0F0]
        
        self.thread_tray_socket = threading.Thread(target=self.have_obj_socket)
        self.thread_tray_socket.daemon = True
        self.thread_tray_socket.start()

    def bing_led(self, addr):
        for color in self.color_rgb:
            if self.bing_picked:
                break
            time.sleep(0.05)
            self.write_register(
                registeraddress=addr, 
                value=color,
                mode=0
            )

    # Check object all socket in hole
    def have_obj_socket(self):
        while True:
            if self.socket_tray_check_obj is False:
                for index in range(len(self.socket_tray)):
                    res_obj_socket_tray = self.read_register(
                        registeraddress = index,
                        numberOfDecimals = 0,
                        functioncode = 4,
                        signed = False
                    )
                    self.socket_tray[index + 1] = res_obj_socket_tray
                    if bool(res_obj_socket_tray) is False and (index + 1) != self.socket_pickup:
                        self.write_register(
                            registeraddress=index, 
                            value=0x00F,
                            mode=0
                        )
                    elif bool(res_obj_socket_tray) is False and (index + 1) == self.socket_pickup:
                        # pick scoket
                        try:
                            self.bing_led(index)
                        except AttributeError:
                            pass
                    elif bool(res_obj_socket_tray) and (index + 1) == self.socket_pickup:
                        self.bing_picked = True
                        self.write_register(
                            registeraddress=index, 
                            value=0x0F0,
                            mode=0
                        )
                    elif bool(res_obj_socket_tray) and (index + 1) != self.socket_pickup:
                        self.bing_picked = True
                        self.write_register(
                            registeraddress=index, 
                            value=0xF00,
                            mode=0
                        )
                self.socket_tray_check_obj = False
                self.bing_picked = True

    def set_socket_pickup(self, value):
        self.socket_pickup = value
        
    def write_register(self, registeraddress, value, mode=0):
        try:
            self.instrument.write_register(registeraddress, value, mode)
        except AttributeError:
            pass

    def read_register(self, registeraddress, mode=0):
        try:
            res_value = self.instrument.read_register(
                registeraddress, 
                mode
            )  # Registernumber, number of decimals
            return hex(res_value)
        except AttributeError:
            pass

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

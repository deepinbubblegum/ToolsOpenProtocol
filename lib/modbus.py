#!/usr/bin/env python3
import minimalmodbus
import serial

class TrayModbus():
    def __init__(self, port='/dev/ttyUSB0', device=0x01, baudrate=19200, bytesize = 8, parity=serial.PARITY_NONE, stopbits=1, timeout=0.05):
        self.instrument = minimalmodbus.Instrument(port, device)  # port name, slave address (in decimal)
        self.instrument.serial.port                     # this is the serial port name
        self.instrument.serial.baudrate = baudrate         # Baud
        self.instrument.serial.bytesize = bytesize
        self.instrument.serial.parity   = parity
        self.instrument.serial.stopbits = stopbits
        self.instrument.serial.timeout  = timeout          # seconds

        self.instrument.address                         # this is the slave address number
        self.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
        self.instrument.clear_buffers_before_each_transaction = True

    def write_register(self, registeraddress, value, mode=1):
        self.instrument.write_register(registeraddress, value, mode)

    def read_register(self, registeraddress, mode=1):
        res_value = self.instrument.read_register(registeraddress, mode)  # Registernumber, number of decimals
        return hex(res_value)

    def read_register(self, registeraddress, numberOfDecimals=0, functioncode=4, signed=False):
        registervalue = self.instrument.read_register(registeraddress, numberOfDecimals, functioncode, False)
        return registervalue

    def close(self):
        self.instrument.serial.close()